# Data

Raw audio is **not** included in this repository. Download the three corpora used
in the paper yourself and place them under `data/raw/`.

## Datasets used in the paper

The three corpora are merged into one large training set, which is what the
reported 97.8% refers to.

| Dataset | Language | Speakers | Emotional classes | Notes |
|---|---|---|---|---|
| RAVDESS | English (North American) | 24 professional actors (12 M / 12 F) | 8 | studio recorded; speech and song |
| TESS | English (North American) | 2 actresses (young / older) | 7 | strong two-speaker bias; pleasant-surprise category |
| CREMA-D | English | 91 actors | 6 | diverse ages and ethnicities; clipped intensity labels |

Each corpus covers a different subset of the eight target emotions. The merged
label space used here is: happy, calm, sad, surprised, neutral, angry, disgust, fear.
`src/labels.py` is the single source of truth for that mapping.

Sources: RAVDESS is distributed via Zenodo; TESS and CREMA-D are available through
their project pages and common mirrors. Each project page states the citation you
must include for the dataset itself, separate from citing the paper.

<!-- FILL: add the exact per-corpus clip counts you used after merging -->

## Expected layout

```
data/
├── raw/
│   ├── ravdess/Actor_01/03-01-05-01-02-01-01.wav
│   ├── tess/OAF_back_angry.wav
│   └── crema-d/1001_DFA_ANG_XX.wav
└── processed/
    └── features.csv        # written by stage 1, read by stage 2
```

## The merged dataset is imbalanced — handle it consciously

RAVDESS, TESS and CREMA-D do not contribute equal numbers of clips per emotion, and
CREMA-D only provides six of the eight classes. Merging them therefore produces a
class distribution skewed toward the emotions all three corpora share.

Two consequences worth documenting in the paper and the notebook:

- Report **macro-averaged F1** alongside accuracy, otherwise the majority classes
  dominate the headline number.
- State whether class weighting, oversampling, or nothing at all was applied during
  training. Whichever it was, it belongs in the paper's method section.

## Feature file (`data/processed/features.csv`)

One row per clip:

| column | meaning |
|---|---|
| `file` | source clip identifier, for traceability |
| `speaker` | speaker / actor id — required for speaker-independent splits |
| `dataset` | `ravdess` / `tess` / `crema-d` — required for cross-corpus experiments |
| `label` | integer class id per `src/labels.py` |
| `zcr` | Zero Crossing Rate |
| `rmse` | Root Mean Square Energy |
| `mfcc_0` ... `mfcc_n` | MFCC coefficients |

Keeping `speaker` and `dataset` as columns is a deliberate design decision: it makes
a speaker-independent or leave-one-corpus-out evaluation possible later **without
re-extracting features**. Those are exactly the experiments that turn this code into
a thesis chapter.

## Downloading with the Kaggle API (optional)

```bash
pip install kaggle
mkdir -p ~/.kaggle && mv kaggle.json ~/.kaggle/ && chmod 600 ~/.kaggle/kaggle.json
kaggle datasets download -d <owner/dataset-slug> -p data/raw --unzip
```

`kaggle.json` is git-ignored — never commit it.
