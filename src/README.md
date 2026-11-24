# src

Small, importable helpers. The goal is not to hide the method in a library — a
reviewer should be able to read the notebooks — but to keep the pieces that must
never diverge out of the notebooks.

| file | status | purpose |
|---|---|---|
| `labels.py` | done | class ids, RAVDESS filename parsing, speaker ids |
| `features.py` | to add | feature extraction and feature-matrix assembly |
| `models.py` | to add | CNN and CNN-BiLSTM definitions |
| `metrics.py` | to add | metric computation and confusion-matrix plotting |

## Suggested path for moving code out of the notebooks

Do this incrementally, one function at a time, verifying the notebook still runs
after each move:

1. Copy the RAVDESS parsing loop into `labels.parse_ravdess` — already done.
2. Copy the extraction function signature (`extract_features(y, sr) -> np.ndarray`)
   into `features.py`.
3. Copy the model build functions into `models.py`.
4. Replace the notebook cell bodies with imports and a short call.

If a helper is used by only one notebook and only once, leave it in the notebook.
Extraction between two notebooks is the strongest reason to move it out.

## Importing from a notebook in Colab

```python
import sys, os
sys.path.append(os.path.abspath(".."))   # when CWD is notebooks/
from src.labels import EMOTIONS, parse_ravdess
```
