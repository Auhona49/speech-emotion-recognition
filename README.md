# Emotion Recognition from Speech Audio Signals using CNN-BiLSTM Hybrid Model

Official code for the paper:

> **Auhona Islam, Md. Ferdouse Ahmed Foysal, Md. Imteaz Ahmed.**
> *Emotion Recognition from Speech Audio Signals using CNN-BiLSTM Hybrid Model.*
> 2024 3rd International Conference on Advancement in Electrical and Electronic Engineering (ICAEEE), IEEE, 2024, pp. 1–6.
> DOI: [10.1109/ICAEEE62219.2024.10561755](https://doi.org/10.1109/ICAEEE62219.2024.10561755)

[Paper (IEEE Xplore)](https://doi.org/10.1109/ICAEEE62219.2024.10561755) ·
[ResearchGate](https://www.researchgate.net/publication/381689422)

---

## Overview

Speech Emotion Recognition (SER) matters for human-computer interaction, human-robot
interaction, behavioural assessment and virtual-reality systems, but emotion is not
easily separable from the physiological signal of speech. Much prior work uses a
single corpus and one feature family, which makes reported accuracy hard to compare.

This work merges **three public corpora — RAVDESS, TESS and CREMA-D — into one large
training set**, extracts **three complementary feature families — Zero Crossing Rate
(ZCR), Root Mean Square Energy (RMSE) and Mel-Frequency Cepstral Coefficients (MFCC)**,
and classifies **eight emotions**: happy, calm, sad, surprised, neutral, angry,
disgust and fear.

Two classifiers are compared:

| Model | Role in the study |
|---|---|
| CNN | baseline over the extracted feature representation |
| **CNN-BiLSTM** | proposed model; the BiLSTM adds temporal modelling on top of convolutional features |

The proposed hybrid model reaches **97.8% accuracy** on the merged three-corpus dataset.

## Pipeline

The study is implemented as two sequential stages. They are separate notebooks
because stage 2 is cheap to re-run, so every classification experiment reuses the
same extracted features instead of repeating the expensive extraction step.

```
RAVDESS + TESS + CREMA-D
          │
          ▼
┌────────────────────────────────────────────────┐
│ Stage 1  notebooks/01_*.ipynb                   │
│  • load and label audio from three corpora      │
│  • extract ZCR, RMSE, MFCC                      │
│  • concatenate into a single feature matrix     │
│  • exploratory visualization                    │
│  • CNN baseline                                 │
└────────────────────────────────────────────────┘
          │
          ▼  features.csv  ← the contract between the two stages
┌────────────────────────────────────────────────┐
│ Stage 2  notebooks/02_*.ipynb                   │
│  • load features.csv                            │
│  • reshape into frame sequences                 │
│  • CNN-BiLSTM training and evaluation           │
└────────────────────────────────────────────────┘
```

`features.csv` is the handoff point: stage 1 writes it once, stage 2 reads it, and
every classification result in the paper traces back to that one file.

## Results

| Model | Features | Corpus | Accuracy |
|---|---|---|---|
| CNN (stage 1) | ZCR + RMSE + MFCC | RAVDESS + TESS + CREMA-D | <!-- FILL: your CNN-only number --> |
| **CNN-BiLSTM (stage 2)** | ZCR + RMSE + MFCC | RAVDESS + TESS + CREMA-D | **97.8%** |

<!-- FILL: add precision / recall / weighted F1 columns if they are in the paper -->

Figures and confusion matrices: `results/figures/`.

## Evaluation protocol — please read

State the split protocol explicitly in this section, because it determines how the
97.8% should be read:

<!-- FILL: choose one and delete the other -->

- [ ] **Random clip-level split** — clips from the same speaker appear in both
  train and test. Report it as such. Accuracy is inflated relative to unseen-speaker
  performance because speaker identity is partially leaked through the features.
- [ ] **Speaker-independent split** — speakers in the test set never appear in
  training. This is the number to compare against cross-corpus SER literature.

Documenting this honestly is stronger than leaving it ambiguous: a reviewer who
works on SER will ask, and a clearly stated protocol protects the result.

## Repository layout

```
.
├── notebooks/
│   ├── 01_feature_extraction_and_cnn.ipynb   # stage 1
│   └── 02_cnn_bilstm_classification.ipynb    # stage 2
├── src/
│   └── labels.py        # class ids + filename parsers for all three corpora
├── data/
│   ├── README.md        # download instructions; audio is NOT committed
│   └── processed/       # features.csv lands here (git-ignored)
├── results/
│   ├── figures/
│   └── tables/
├── checkpoints/         # weights (git-ignored)
└── requirements.txt
```

## Data

Raw audio is not redistributed here for licensing reasons. See `data/README.md`.

Expected layout:

```
data/raw/ravdess/Actor_01/03-01-05-01-02-01-01.wav
data/raw/tess/OAF_back_angry.wav
data/raw/crema-d/1001_DFA_ANG_XX.wav
```

## Reproducing

### On Google Colab (primary workflow)

1. Open this repo in Colab, or clone it into Drive.
2. Run `notebooks/01_*.ipynb` top to bottom → writes `data/processed/features.csv`.
3. Run `notebooks/02_*.ipynb` top to bottom → trains the CNN-BiLSTM.

Feature extraction is the slow, I/O-bound step. Copy the audio corpora to the local
`/content` disk before running stage 1 rather than reading them off a Drive mount.

### Locally

```bash
git clone <this-repo-url>
cd speech-emotion-recognition
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

## Citation

```bibtex
@inproceedings{islam2024emotion,
  title     = {Emotion Recognition from Speech Audio Signals using {CNN-BiLSTM} Hybrid Model},
  author    = {Islam, Auhona and Foysal, Md. Ferdouse Ahmed and Ahmed, Md. Imteaz},
  booktitle = {2024 3rd International Conference on Advancement in Electrical and Electronic Engineering (ICAEEE)},
  pages     = {1--6},
  year      = {2024},
  doi       = {10.1109/ICAEEE62219.2024.10561755}
}
```

## Contact

Auhona Islam — islamauhona@gmail.com
