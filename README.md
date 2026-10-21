# MMA3001 Project

Investigating whether encoded depth improves summer apple-tree trunk and
main-branch segmentation compared with RGB alone. Intended use: an initial
perception stage for agricultural robots. This is not a complete picking system,
metric 3D reconstruction, or a safety-validated robot obstacle detector.

## Current status

Dataset audit and initial Gaussian naive Bayes RGB/RGB+depth baselines are
implemented. Scored experiments are deliberately blocked until mask geometry is
confirmed. The GT images are 256x256 while example inputs are 640x480; resizing
without checking crops/alignment would make scores misleading. Depth encoding,
units, mask meaning and dataset redistribution rights remain unconfirmed.

## Setup and reproduction

Python 3.10 or newer. From the repository root:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts/verify.py
python -m appletree audit --archive "C:\path\to\dataset.zip"
```

The audit reads the ZIP without extracting images and writes `artifacts/audit.json`
and `artifacts/manifest.json`. Keep the original archive locally; do not upload it.
The manifest records its SHA-256 and deterministic tree-grouped splits.

ONLY after confirming that each GT is a full-frame resized correspondence:

```powershell
python -m appletree pilot --archive "C:\path\to\dataset.zip" --confirm-full-frame-alignment
```

If masks are crops or warped images, implement that documented transformation
instead; do not use the confirmation switch. The pilot fits both models using
identical random pixel samples from eight training trees, tunes a threshold on
eight validation trees, and evaluates on eight held-out trees. Outputs include
model arrays, per-image and pooled metrics, timing and software versions. This
small pilot is not the final experiment. Do not repeatedly tune against test results.

## Inputs and outputs

Input: university ZIP with tree/season/modality/timestamp PNG names. Exact matched
RGB/D/GT triplets only; unmatched labelled records are reported. Encoded depth is
used as three normalized image channels, not metres. No meaning is assigned to
zero until documentation is obtained. Unsupported formats fail explicitly.
Output: binary masks conceptually; the current CLI saves model parameters and
metric tables as JSON/NPZ. Pixel-location features are excluded to avoid learning
only the centred-tree label layout. Normalization is division by 255.

Gaussian naive Bayes estimates class means/variances and empirical priors, with
a variance floor and log-density calculations. RGB versus RGB+depth uses the same
classifier so the comparison isolates the added encoded-depth information.

## Project records

- [Assessment checklist](docs/checklist.md)
- [Implementation and experiment plan](docs/plan.md)
- [AI-use log](docs/ai_use.md)
- [Data questions and limitations](docs/data_questions.md)
- [Report outline](docs/report_outline.md)
- Generated API HTML: `docs/html/appletree.data.html`, `appletree.model.html`,
  `appletree.metrics.html`; regenerate with `python scripts/verify.py`.
- Test evidence: `docs/test_report.json`.

## Sources and rights

Assessment requirements: MMA3001_2026_Project_Brief (2).pdf, supplied by student,
especially pp. 4-9 and rubric pp. 10-15. Topic scope: Dataset 1 in
https://docs.google.com/presentation/d/1K6hscMh6MUrsN62GauOhGDptcdGuO0vqZ3VrGahZNkQ/edit
Data: supplied university Apple Tree RGBD ZIP; no data is distributed here.
Code: MIT; see LICENSE. AI contribution is recorded separately and requires
student verification and understanding before submission.
