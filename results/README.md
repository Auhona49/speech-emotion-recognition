# Results

Everything a reviewer or an advisor should be able to look at without running code.

```
results/
├── figures/     training curves, confusion matrices, feature plots
└── tables/      metrics as CSV, one row per model/seed
```

## Naming convention

```
figures/cnn_confusion_matrix.png
figures/cnn_bilstm_confusion_matrix.png
figures/cnn_bilstm_training_curves.png
figures/class_distribution.png
tables/model_comparison.csv
tables/per_class_metrics.csv
```

## `tables/model_comparison.csv`

Long format, one row per run, so the mean and std can be computed from the file
instead of being copied by hand:

```csv
model,seed,accuracy,macro_f1,weighted_f1
cnn,42,0.000,0.000,0.000
cnn_bilstm,42,0.000,0.000,0.000
```

Populate this from the notebooks with `to_csv`, never by typing numbers into the
README. Then the README table and the paper table both trace back to one file.

## What to commit

Commit figures and tables. Do not commit model checkpoints — they are
regenerable and belong in the release assets or on Zenodo if the paper needs them.
