"""
Golden constants for SchellingChords M4 tests.
Distance metric: Jaccard distance = 1 - |A ∩ B| / |A ∪ B|, normalised to [0, 1].
Identical chords -> 0.0, disjoint chords -> 1.0.
"""

DIATONIC_CHORDS: dict[str, list[int]] = {
    "C": [0, 4, 7],
    "Dm": [2, 5, 9],
    "Em": [4, 7, 11],
    "F": [0, 5, 9],
}

OVERLAP_COUNTS: dict[tuple[str, str], int] = {
    ("C", "C"): 3, ("C", "Dm"): 0, ("C", "Em"): 2, ("C", "F"): 1,
    ("Dm", "Dm"): 3, ("Dm", "Em"): 0, ("Dm", "F"): 2,
    ("Em", "Em"): 3, ("Em", "F"): 0,
    ("F", "F"): 3,
}

DISTANCES: dict[tuple[str, str], float] = {
    ("C", "C"): 0.0, ("C", "Dm"): 1.0, ("C", "Em"): 0.5, ("C", "F"): 0.8,
    ("Dm", "Dm"): 0.0, ("Dm", "Em"): 1.0, ("Dm", "F"): 0.5,
    ("Em", "Em"): 0.0, ("Em", "F"): 1.0,
    ("F", "F"): 0.0,
}
