"""Single source of truth for label mapping and corpus filename parsing.

Both notebooks import from here so that class ids, class names and speaker ids are
identical in the feature CSV and in the classifier. If the two stages disagree on
label order, every confusion matrix in the paper is silently wrong.

Corpora used in the paper: RAVDESS, TESS, CREMA-D (merged).
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Canonical class list, in the order used in the paper.
# ORDER MATTERS: it defines the integer ids written to features.csv.
# ---------------------------------------------------------------------------
EMOTIONS = [
    "happy",
    "calm",
    "sad",
    "surprised",
    "neutral",
    "angry",
    "disgust",
    "fear",
]

LABEL_TO_ID = {name: i for i, name in enumerate(EMOTIONS)}
ID_TO_LABEL = {i: name for name, i in LABEL_TO_ID.items()}

N_CLASSES = len(EMOTIONS)


# ---------------------------------------------------------------------------
# RAVDESS
# Filename: 03-01-05-01-02-01-01.wav
#   modality-vocal-channel-emotion-intensity-statement-repetition-actor
# ---------------------------------------------------------------------------
RAVDESS_EMOTION_CODES = {
    "01": "neutral",
    "02": "calm",
    "03": "happy",
    "04": "sad",
    "05": "angry",
    "06": "fear",
    "07": "disgust",
    "08": "surprised",
}


def parse_ravdess(path: str | Path) -> dict:
    stem = Path(path).stem
    parts = stem.split("-")
    if len(parts) != 7:
        raise ValueError(f"not a RAVDESS filename: {stem}")
    modality, _vocal, _channel, emotion, intensity, _statement, actor = parts
    return {
        "file": stem,
        "dataset": "ravdess",
        "speaker": f"ravdess_{int(actor):02d}",
        "gender": "male" if int(actor) % 2 == 1 else "female",
        "label": LABEL_TO_ID[RAVDESS_EMOTION_CODES[emotion]],
        "modality": "speech" if modality == "03" else "song",
        "intensity": "strong" if intensity == "02" else "normal",
    }


# ---------------------------------------------------------------------------
# TESS
# Filename: OAF_back_angry.wav  ->  speaker_word_emotion
# Speakers: YAF = young adult female, OAF = older adult female.
# ---------------------------------------------------------------------------
TESS_EMOTIONS = {
    "angry": "angry",
    "disgust": "disgust",
    "fear": "fear",
    "happy": "happy",
    "neutral": "neutral",
    "sad": "sad",
    "pleasant_surprise": "surprised",
    "pleasantsurprise": "surprised",
    "surprise": "surprised",
}


def parse_tess(path: str | Path) -> dict:
    stem = Path(path).stem.lower()
    parts = stem.split("_")
    speaker, emotion_raw = parts[0], "_".join(parts[2:]) if len(parts) > 2 else ""
    if emotion_raw not in TESS_EMOTIONS:
        # tolerate names like "OAF_back_pleasant_surprise"
        emotion_raw = parts[-2] + "_" + parts[-1] if len(parts) >= 2 else emotion_raw
    return {
        "file": stem,
        "dataset": "tess",
        "speaker": f"tess_{speaker}",
        "gender": "female",
        "label": LABEL_TO_ID[TESS_EMOTIONS[emotion_raw]],
        "modality": "speech",
        "intensity": "normal",
    }


# ---------------------------------------------------------------------------
# CREMA-D
# Filename: 1001_DFA_ANG_XX.wav  ->  actor_sentence_emotion_intensity
# Note: CREMA-D covers only six emotions, so it contributes no calm/surprised clips.
# ---------------------------------------------------------------------------
CREMAD_EMOTION_CODES = {
    "ANG": "angry",
    "DIS": "disgust",
    "FEA": "fear",
    "HAP": "happy",
    "NEU": "neutral",
    "SAD": "sad",
}


def parse_cremad(path: str | Path) -> dict:
    stem = Path(path).stem
    parts = stem.split("_")
    if len(parts) != 4:
        raise ValueError(f"not a CREMA-D filename: {stem}")
    actor, _sentence, emotion, intensity = parts
    return {
        "file": stem,
        "dataset": "crema-d",
        "speaker": f"cremad_{actor}",
        "gender": "unknown",  # CREMA-D gender is metadata, not encoded in the name
        "label": LABEL_TO_ID[CREMAD_EMOTION_CODES[emotion.upper()]],
        "modality": "speech",
        "intensity": {"LO": "low", "MD": "medium", "HI": "high"}.get(intensity.upper(), "unspecified"),
    }


PARSERS = {
    "ravdess": parse_ravdess,
    "tess": parse_tess,
    "crema-d": parse_cremad,
}


def parse_any(path: str | Path, dataset: str) -> dict:
    return PARSERS[dataset](path)


# ---------------------------------------------------------------------------
# Speaker-aware splitting helper: keeps every speaker in exactly one split.
# ---------------------------------------------------------------------------
def speaker_split(speakers, test_size=0.2, seed=42):
    """Return (train_speakers, test_speakers), disjoint."""
    import numpy as np

    uniq = sorted(set(speakers))
    rng = np.random.default_rng(seed)
    rng.shuffle(uniq)
    n_test = max(1, int(round(len(uniq) * test_size)))
    return set(uniq[n_test:]), set(uniq[:n_test])
