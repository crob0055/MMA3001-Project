# Plan

Question: Does encoded depth improve summer trunk/main-branch segmentation over
RGB alone? Primary engineering context: perception for agricultural robots.

1. Foundation (started): audit ZIP, exact triplets, reproducible identity split,
   transparent RGB and RGB+depth baselines, tests, HTML documentation, GitHub.
   Completion evidence: audit.json, manifest, test report and working commands.
2. Establish label validity: obtain mask meaning/crop transform and depth encoding.
   Check overlays across several rows and trees. If full-frame correspondence is
   false, implement the supplied transformation before any scored training.
   Confirm whether segmentation alone satisfies the chosen topic expectations.
3. Pilot: run matched small experiments with identical training samples and
   splits. Inspect overlays, labels, foreground imbalance, depth failure and
   spatial bias. Consider a stronger classifier only if the evidence warrants it.
4. Freeze protocol: document train/validation/test split, grouping, hyperparameters,
   sampling, threshold-selection rule and primary metric. Consider holding out
   whole orchard rows; adjacent images may overlap despite distinct tree IDs.
5. Experiments: RGB vs RGB+encoded-depth ablation; validation-only sensitivity to
   threshold, resolution and sample count. Profile loading separately from fitting
   and inference. Evaluate the frozen selected settings on test once. Report paired
   per-tree differences and bootstrap intervals over trees (or rows if grouped).
6. Delivery: failure-case figures, final 5-10 page report, AI reflection, regenerated
   API docs/test report, clean-environment reproduction, repository link and zipped
   clone, 5-minute presentation and oral explanation practice.

Initial model: Gaussian naive Bayes on RGB or RGB+3 depth-code channels, class
priors estimated from uniform sampled training pixels, variance floor 1e-4.
Threshold grid 0.1 to 0.9 selected by pooled validation IoU. No spatial coordinates,
metres, apple labels, hidden-branch completeness or 3D accuracy are inferred.

Extension only after core validation: skeletonize the predicted binary mask and
evaluate branch connectivity against an appropriate reference. A 2D skeleton
does not establish a metric 3D skeleton.

No fixed calendar milestones yet: due dates and remaining time must come from the
unit overview. The brief has no formal intermediate project milestones.
