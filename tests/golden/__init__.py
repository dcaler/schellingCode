# Frozen golden values for SchellingChords M6 sonification tests.
# All values are hand-derived and internally consistent.

# Diatonic triads as sorted pitch-class sets (0..11)
DIATONIC_CHORDS: dict[str, list[int]] = {
    "C":  [0, 4, 7],
    "Dm": [2, 5, 9],
    "Em": [4, 7, 11],
}

# Intersection sizes |A ∩ B|
OVERLAP_COUNTS: dict[tuple[str, str], int] = {
    ("C",  "C"):  3, ("C",  "Dm"): 0, ("C",  "Em"): 2,
    ("Dm", "C"):  0, ("Dm", "Dm"): 3, ("Dm", "Em"): 0,
    ("Em", "C"):  2, ("Em", "Dm"): 0, ("Em", "Em"): 3,
}

# Jaccard distance: 1 - |A ∩ B| / |A ∪ B|
# Normalised to [0, 1] where identical -> 0.0 and disjoint -> 1.0
DISTANCES: dict[tuple[str, str], float] = {
    ("C",  "C"):  0.0, ("C",  "Dm"): 1.0, ("C",  "Em"): 0.5,
    ("Dm", "C"):  1.0, ("Dm", "Dm"): 0.0, ("Dm", "Em"): 1.0,
    ("Em", "C"):  0.5, ("Em", "Dm"): 1.0, ("Em", "Em"): 0.0,
}

# 1D window fixture constants
# 4 bars * 4 beats/bar = 16 beat-slots
WINDOW_TOTAL_SLOTS: int = 16
# Flat list of 0/1 per beat. 1 = occupied chord, 0 = vacancy/rest
WINDOW_SLOTS: list[int] = [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0]
WINDOW_OCCUPIED_INDICES: list[int] = [0, 2, 5, 7, 10, 12]
WINDOW_OCCUPIED_SLOTS: int = len(WINDOW_OCCUPIED_INDICES)
# Invariant: WINDOW_OCCUPIED_SLOTS + (WINDOW_TOTAL_SLOTS - WINDOW_OCCUPIED_SLOTS) == WINDOW_TOTAL_SLOTS
