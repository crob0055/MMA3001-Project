"""CLI: audit the private ZIP, or run an explicitly geometry-confirmed pilot."""
import argparse
import collections
import hashlib
import json
import platform
import time
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import PIL

from .data import inventory, split_records, read_image, load_record
from .metrics import confusion, scores
from .model import features, GaussianPixels


def main():
    """Run audit or pilot; write JSON provenance without copying source images."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["audit", "pilot"])
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("artifacts"))
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--confirm-full-frame-alignment", action="store_true")
    parser.add_argument("--trees-per-split", type=int, default=8)
    parser.add_argument("--pixels-per-image", type=int, default=2000)
    args = parser.parse_args()
    if args.trees_per_split < 1 or args.pixels_per_image < 1:
        parser.error("Sample limits must be positive")
    if args.command == "pilot" and not args.confirm_full_frame_alignment:
        parser.error("Pilot blocked: establish full-frame mask correspondence first")
    records, issues = inventory(args.archive)
    splits = split_records(records, args.seed)
    args.output.mkdir(parents=True, exist_ok=True)
    with args.archive.open("rb") as stream:
        digest = hashlib.sha256()
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    provenance = dict(archive_sha256=digest.hexdigest(), seed=args.seed,
                      python=platform.python_version(), numpy=np.__version__, pillow=PIL.__version__)
    manifest = dict(provenance=provenance, issues=issues, splits=splits)
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    with ZipFile(args.archive) as source:
        if args.command == "audit":
            summaries = collections.Counter()
            for record in records:
                for kind, member in record["files"].items():
                    a = read_image(source, member)
                    summaries[(kind, str(a.shape), str(a.dtype))] += 1
            report = dict(provenance=provenance, labelled_records=len(records), issues=issues,
                          image_formats=[dict(kind=k[0], shape=k[1], dtype=k[2], count=v) for k,v in summaries.items()],
                          split_counts={k: len(v) for k,v in splits.items()},
                          status="Geometry and depth encoding unconfirmed; no scored results")
            (args.output / "audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
            print(json.dumps({k:v for k,v in report.items() if k != "issues"}, indent=2))
            return
        # A pilot is deliberately small. Never label this the final experiment.
        selected = {}
        for part, rows in splits.items():
            ids = sorted({r["tree"] for r in rows})[:args.trees_per_split]
            selected[part] = [r for r in rows if r["tree"] in ids]
        result = dict(provenance=provenance, status="Pilot only; user confirmed full-frame geometry",
                      selected_ids={k: sorted({r['tree'] for r in v}) for k,v in selected.items()}, methods={})
        for mode in ("rgb", "rgb_depth"):
            rng = np.random.default_rng(args.seed)
            xs, ys = [], []
            start = time.perf_counter()
            for record in selected["train"]:
                rgb, depth, mask = load_record(source, record, True)
                x = features(rgb, depth if mode == "rgb_depth" else None)
                indices = rng.choice(len(x), min(len(x), args.pixels_per_image), replace=False)
                xs.append(x[indices]); ys.append(mask.ravel()[indices])
            model = GaussianPixels().fit(np.concatenate(xs), np.concatenate(ys))
            train_seconds = time.perf_counter() - start
            cached = []
            for record in selected["validation"]:
                rgb, depth, mask = load_record(source, record, True)
                cached.append((mask.ravel(), model.predict_proba(features(rgb, depth if mode == "rgb_depth" else None))))
            thresholds = np.linspace(.1, .9, 9)
            validation = [scores(sum((confusion(y, p >= t) for y,p in cached), np.zeros(4, dtype=int)))["iou"] for t in thresholds]
            threshold = float(thresholds[int(np.argmax(validation))])
            start = time.perf_counter()
            rows = []
            for record in selected["test"]:
                rgb, depth, mask = load_record(source, record, True)
                p = model.predict_proba(features(rgb, depth if mode == "rgb_depth" else None))
                counts = confusion(mask.ravel(), p >= threshold)
                rows.append(dict(tree=record["tree"], counts=counts.tolist(), **scores(counts)))
            result["methods"][mode] = dict(threshold=threshold, validation_iou=max(validation),
                train_seconds=train_seconds, evaluation_seconds=time.perf_counter()-start,
                pooled=scores(np.sum([r["counts"] for r in rows], axis=0)), per_image=rows)
            np.savez(args.output / f"{mode}_model.npz", mean=model.mean, var=model.var, prior=model.prior, threshold=threshold)
        (args.output / "pilot.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
