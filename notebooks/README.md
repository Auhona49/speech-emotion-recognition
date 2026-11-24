# Notebooks

Two notebooks, two stages, one pipeline. Run in numeric order.

## `01_feature_extraction_and_cnn.ipynb` — stage 1

Input: raw audio from `data/raw/{ravdess,tess,crema-d}/`.
Output: `data/processed/features.csv`, plots in `results/figures/`, CNN-baseline metrics.

Expected sections, in this order:

1. Setup — installs, imports, optional Drive mount (guarded so it also runs locally)
2. Configuration — all paths, seed, and hyperparameters as UPPERCASE constants
3. Corpus loading and label parsing via `src.labels` (all three datasets)
4. Feature extraction — ZCR, RMSE, MFCC; the slow loop, cache the result
5. Merge into one feature matrix and export to `features.csv`
6. Exploratory visualization — class balance per corpus, feature distributions,
   correlation between the three feature families
7. CNN-only baseline — split, train, evaluate, log metrics to `results/tables/`

## `02_cnn_bilstm_classification.ipynb` — stage 2

Input: `data/processed/features.csv` only. No audio access needed.
Output: CNN-BiLSTM metrics (97.8% reported), training curves, confusion matrix.

Because this stage is cheap, all hyperparameter search and ablation belongs here.

## Conventions that make this reviewable

- **Runs top-to-bottom on a fresh runtime.** No variable inherited from a deleted cell.
- **One config cell.** Paths, seed, epochs, batch size, split protocol, all in one place.
- **Seeds set once,** for `random`, `numpy` and the framework. Report mean ± std over
  at least 3 seeds — a single 97.8% run is weaker evidence than 97.8 ± 0.4 over five.
- **The split is explicit and saved.** Write the train/test index list to disk and load
  it in stage 2. An implicit `train_test_split` call cannot be reproduced after the fact,
  and the split protocol decides how the accuracy should be interpreted.
- **Label order comes from `src.labels`.** Never retype the emotion list in a notebook.
- **Class imbalance is visible.** Print `value_counts()` per corpus after merging and
  state what you did about it (weights, oversampling, or nothing).
- **Clear outputs before committing.** `Cell > All Output`, or
  `jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace`.
  Colab stores Drive paths, and sometimes your email, in cell metadata.
- **One setup cell,** not `!pip install` in every cell.

## On moving files out of Colab

Colab notebooks are files like any other: `File > Download > Download .ipynb`, or
`File > Save a copy in GitHub` to push straight into this repo. Keep the canonical copy
in GitHub and treat Colab as the runtime — that way a lost runtime never loses work.
