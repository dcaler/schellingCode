"""
Golden values for SchellingChords tests.

Jaccard distance formula: distance(a, b) = 1 - |a ∩ b| / |a ∪ b|
All diatonic triads have cardinality 3, so |a ∪ b| = 6 - |a ∩ b|.
Identical chords -> distance 0.0, disjoint chords -> distance 1.0.
"""

DIATONIC_CHORDS: dict[str, list[int]] = {
    "C": [0, 4, 7],
    "Dm": [2, 5, 9],
    "Em": [4, 7, 10],
    "F": [0, 5, 9],
    "G": [2, 7, 10],
    "Am": [0, 4, 9],
    "Bdim": [2, 5, 10],
}

OVERLAP_COUNTS: dict[tuple[str, str], int] = {
    ("C", "Dm"): 0,
    ("C", "Em"): 2,
    ("C", "F"): 1,
    ("C", "G"): 1,
    ("C", "Am"): 2,
    ("C", "Bdim"): 0,
    ("Dm", "Em"): 0,
    ("Dm", "F"): 2,
    ("Dm", "G"): 1,
    ("Dm", "Am"): 1,
    ("Dm", "Bdim"): 2,
    ("Em", "F"): 0,
    ("Em", "G"): 2,
    ("Em", "Am"): 1,
    ("Em", "Bdim"): 1,
    ("F", "G"): 0,
    ("F", "Am"): 2,
    ("F", "Bdim"): 1,
    ("G", "Am"): 0,
    ("G", "Bdim"): 2,
    ("Am", "Bdim"): 0,
}

DISTANCES: dict[tuple[str, str], float] = {
    ("C", "Dm"): 1.0,
    ("C", "Em"): 0.5,
    ("C", "F"): 0.8,
    ("C", "G"): 0.8,
    ("C", "Am"): 0.5,
    ("C", "Bdim"): 1.0,
    ("Dm", "Em"): 1.0,
    ("Dm", "F"): 0.5,
    ("Dm", "G"): 0.8,
    ("Dm", "Am"): 0.8,
    ("Dm", "Bdim"): 0.5,
    ("Em", "F"): 1.0,
    ("Em", "G"): 0.5,
    ("Em", "Am"): 0.8,
    ("Em", "Bdim"): 0.8,
    ("F", "G"): 1.0,
    ("F", "Am"): 0.5,
    ("F", "Bdim"): 0.8,
    ("G", "Am"): 1.0,
    ("G", "Bdim"): 0.5,
    ("Am", "Bdim"): 1.0,
}

# 1D Window fixture constants
WINDOW_TOTAL_SLOTS = 16
WINDOW_SLOTS = [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1]
WINDOW_OCCUPIED_INDICES = [0, 1, 3, 4, 5, 7, 8, 9, 10, 12, 13, 15]
WINDOW_VACANT_INDICES = [2, 6, 11, 14]
WINDOW_OCCUPIED_COUNT = 12
WINDOW_VACANT_COUNT = 4
