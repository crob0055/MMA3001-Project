# Initial dataset audit

Executed against supplied ZIP on 2026-10-22 using the appletree audit command.
562 exact timestamp/tree/folder RGB/D/GT triplets; no incomplete labelled groups.
All 562 RGB and all 562 D inputs are 480x640x3 uint8. All 562 GT inputs are
256x256 uint8 single-channel. This confirms dimensions, not mask semantics.

Seed 42 split: 337 train, 112 validation, 113 test. Grouped by tree identity.
No segmentation scores produced. Full local manifest/audit are in artifacts/,
excluded from Git along with data and model output.

Archive SHA-256:
ed9fadbd8a6b69f0d502ea0527b0bf2d865aa2075ca05466fab0e45baeb0d088

Runtime: Python 3.12.14, NumPy 2.3.5, Pillow 12.3.0.
