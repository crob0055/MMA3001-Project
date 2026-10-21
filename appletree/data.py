"""Read RGB, encoded depth and masks directly from the supplied ZIP.

No source images are extracted or redistributed. Filename identities are the
available grouping evidence, not proof that different IDs are unrelated trees.
"""
import io
import random
import re
from collections import defaultdict
from pathlib import PurePosixPath
from zipfile import ZipFile

import numpy as np
from PIL import Image

PATTERN = re.compile(r"(?P<tree>R\d+[A-Za-z]+\d+)_(?P<season>Summer|Winter)_(?P<kind>RGB|D|GT)-(?P<time>.+)\.png$")


def inventory(archive):
    """Return complete labelled summer records and audit issues.

    Args:
        archive: Path to the original dataset ZIP.
    Returns:
        Tuple of record dictionaries and issues. Exact folder, tree, season and
        timestamp must match. Duplicate modalities raise ValueError.
    """
    groups = defaultdict(dict)
    with ZipFile(archive) as source:
        for name in source.namelist():
            path = PurePosixPath(name)
            match = PATTERN.fullmatch(path.name)
            if not match:
                continue
            tree, season, kind, timestamp = match.group("tree", "season", "kind", "time")
            key = (str(path.parent), tree, season, timestamp)
            if kind in groups[key]:
                raise ValueError(f"Duplicate {kind}: {key}")
            groups[key][kind] = name
    records, issues = [], []
    for (folder, tree, season, timestamp), files in sorted(groups.items()):
        if "GT" not in files:
            continue
        missing = sorted({"RGB", "D", "GT"} - files.keys())
        if missing:
            issues.append({"tree": tree, "timestamp": timestamp, "missing": missing})
            continue
        records.append(dict(tree=tree, season=season, timestamp=timestamp,
                            folder=folder, files=files))
    if not records:
        raise ValueError("No exactly matched RGB/D/GT records found")
    return records, issues


def split_records(records, seed=42):
    """Return deterministic 60/20/20 train/validation/test groups by tree ID.

    All observations sharing a tree ID stay together, including across folders.
    Raises ValueError when fewer than five unique trees are available.
    """
    trees = sorted({r["tree"] for r in records})
    if len(trees) < 5:
        raise ValueError("At least five tree identities required")
    random.Random(seed).shuffle(trees)
    n_train, n_val = int(.6 * len(trees)), max(1, int(.2 * len(trees)))
    assignment = {t: ("train" if i < n_train else "validation" if i < n_train + n_val else "test")
                  for i, t in enumerate(trees)}
    return {part: [r for r in records if assignment[r["tree"]] == part]
            for part in ("train", "validation", "test")}


def read_image(source, member):
    """Return a copied NumPy image array from an open ZipFile member."""
    with Image.open(io.BytesIO(source.read(member))) as image:
        return np.array(image)


def load_record(source, record, alignment_confirmed=False):
    """Load a pair at mask resolution ONLY after full-frame alignment is confirmed.

    Args:
        source: Open ZipFile.
        record: An inventory record.
        alignment_confirmed: Caller has independently established that masks
            correspond to full-frame resized inputs, rather than a crop/warp.
    Returns:
        RGB uint8, encoded-depth uint8 RGB and boolean target mask arrays.
        Depth values are image codes, never metres. Zero is not assumed invalid.
    Raises:
        ValueError: Alignment unconfirmed, unsupported shapes or nonbinary mask.
    """
    if not alignment_confirmed:
        raise ValueError("Confirm mask geometry before training or evaluation")
    rgb, depth, mask = [read_image(source, record["files"][k]) for k in ("RGB", "D", "GT")]
    if mask.ndim != 2 or not set(np.unique(mask)).issubset({0, 255}):
        raise ValueError("Expected binary 0/255 single-channel GT")
    for name, array in (("RGB", rgb), ("D", depth)):
        if array.ndim != 3 or array.shape[2] != 3 or array.dtype != np.uint8:
            raise ValueError(f"Unsupported {name} encoding: {array.shape}, {array.dtype}")
    if rgb.shape != depth.shape:
        raise ValueError("RGB/D source shapes differ")
    size = (mask.shape[1], mask.shape[0])
    # Nearest-neighbour avoids inventing intermediate encoded-depth values.
    rgb = np.array(Image.fromarray(rgb).resize(size, Image.Resampling.BILINEAR))
    depth = np.array(Image.fromarray(depth).resize(size, Image.Resampling.NEAREST))
    return rgb, depth, mask > 0
