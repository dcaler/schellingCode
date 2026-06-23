"""Golden constants for M2 distance metric tests."""
from typing import Dict, List, Tuple

# Diatonic major triads in C major (pitch classes 0=C, 1=D, ..., 11=B)
DIATONIC_CHORDS: Dict[str, List[int]] = {
    "I": [0, 2, 4],
    "ii": [1, 3, 5],
    "iii": [2, 4, 6],
    "IV": [0, 3, 5],
    "V": [1, 4, 6],
    "vi": [0, 2, 5],
    "vii°": [1, 3, 6],
}

# Intersection sizes |A ∩ B|
OVERLAP_COUNTS: Dict[Tuple[str, str], int] = {
    ("I", "I"): 3,
    ("I", "V"): 1,
    ("I", "vii°"): 0,
    ("I", "iii"): 2,
    ("V", "vii°"): 2,
    ("ii", "vi"): 1,
}

# Jaccard distance: 1 - |A ∩ B| / |A ∪ B|
# Since |A|=|B|=3, |A ∪ B| = 6 - overlap
DISTANCES: Dict[Tuple[str, str], float] = {
    ("I", "I"): 0.0,
    ("I", "V"): 1 - 1 / 5,  # 0.8
    ("I", "vii°"): 1.0,
    ("I", "iii"): 1 - 2 / 4,  # 0.5
    ("V", "vii°"): 1 - 2 / 4,  # 0.5
    ("ii", "vi"): 1 - 1 / 5,  # 0.8
}

# 1D Window fixture constants (bars_per_window=4 -> 16 beat-slots)
WINDOW_TOTAL_SLOTS = 16
WINDOW_SLOTS = [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0]
WINDOW_OCCUPIED_INDICES = [i for i, v in enumerate(WINDOW_SLOTS) if v == 1]
WINDOW_VACANT_INDICES = [i for i, v in enumerate(WINDOW_SLOTS) if v == 0]
WINDOW_OCCUPIED_SLOTS = len(WINDOW_OCCUPIED_INDICES)
WINDOW_VACANT_SLOTS = len(WINDOW_VACANT_INDICES)

# Consistency assertions (fail at import if wrong)
assert WINDOW_TOTAL_SLOTS == len(WINDOW_SLOTS), "Window total slots mismatch"
assert WINDOW_OCCUPIED_SLOTS + WINDOW_VACANT_SLOTS == WINDOW_TOTAL_SLOTS, "Occupied + vacant != total"
