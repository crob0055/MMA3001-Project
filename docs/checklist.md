# Assignment checklist

Source: supplied MMA3001 project brief, 15 pages. This is a working checklist,
not a claim that the assessment has been completed. Dates must be checked in the
unit overview; no due dates are invented here. Project weight: 25% (p. 1).

## Engineering definition and methods (pp. 2, 4-7; rubric pp. 10, 14)
- [x] Draft a focused engineering question and initial scope in README.
- [ ] Confirm segmentation scope fits the suggested project with teaching team.
- [ ] Connect the implemented method to a technique taught in the unit.
- [ ] Finalise intended use, assumptions, limitations and mechanical engineering relevance.
- [ ] Specify input formats, units, domains, missing/invalid input behaviour.
- [ ] Define outputs and their meaning; do not claim metres without calibration.
- [x] Implement an initial functioning method and credible RGB-only comparison.
- [ ] Explain method mathematics, assumptions, parameter choices and alternatives.
- [ ] Compare original/baseline and selected/improved method quantitatively.

## Data, verification and validation (pp. 4-6; rubric p. 13)
- [x] Implement exact file pairing and identity-grouped reproducible splits.
- [ ] Confirm GT semantics, image geometry and depth encoding with teaching team.
- [ ] Visually verify representative RGB/D/GT correspondences after transformation.
- [ ] Confirm whether tree IDs or neighbouring orchard rows require stronger grouping.
- [ ] Audit labels, missing depth, duplicate images, data ownership and licence.
- [x] Implement metric, leakage, numerical stability and geometry-gate tests.
- [x] Run and review initial tests and generate test report; repeat after material changes.
- [ ] Run a small validated pilot, review failure cases, then freeze final protocol.
- [ ] Tune only on training/validation data; keep final test data untouched.
- [ ] Report IoU, Dice, precision/recall, per-tree results and uncertainty.
- [ ] Discuss what validation establishes and what it cannot establish.
- [ ] Analyse runtime with timing/profiling; memory/FLOPS only if useful.
- [ ] Run justified sensitivity studies (threshold, resolution, sample count, depth ablation).
- [ ] Interpret engineering trade-offs, failure modes and lessons honestly.

## Repository deliverables (p. 8; rubric pp. 11-12)
- [x] Create README, dependencies, logical package structure and code licence.
- [x] Provide consistent function docstrings and useful implementation comments.
- [x] Generate initial HTML source-code documentation; review/regenerate as code evolves.
- [ ] Establish GitHub repository and functional main branch.
- [ ] Maintain meaningful development commits and clean reproducibility instructions.
- [ ] Reproduce workflow from a fresh environment and check dependencies.
- [ ] Provide accessible final repository link to assessor.
- [ ] Submit zipped CLONE of repository through Moodle; check data-access instructions.

## Report and AI reflection (pp. 6, 8; rubric p. 15)
- [ ] Write 5-10 page report, maximum 10 pages excluding references/appendices.
- [ ] Cover problem, data/I/O, approach, validation/results, comparison/optimisation.
- [ ] Cover limitations, lessons, references and AI-use reflection.
- [x] Start AI-use log; initial implementation is materially AI-authored.
- [ ] Record tools, tasks, contribution level, reasons, verification and AI errors.
- [ ] Explain student decisions and impact on understanding/workflow.
- [ ] Student independently reviews all code, claims, results and references.
- [ ] Submit report via Moodle by the confirmed deadline.

## Presentation (p. 9)
- [ ] Prepare and rehearse 5-minute individual presentation plus 3-minute questions.
- [ ] Demonstrate repository structure, code documentation, testing and validation.
- [ ] Explain method choice, problem/I/O, limitations/learning and AI evaluation.
- [ ] Practise explaining numerical assumptions, stability, errors and validation unaided.
- [ ] Book and attend Week 14 examination-period appointment; verify final schedule.
