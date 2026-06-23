# Jaccard distance: distance(a,b) = 1 - |a ∩ b| / |a ∪ b|
# Identical chords -> 0.0, Disjoint chords -> 1.0

DIATONIC_CHORDS: dict[str, list[int]] = {
    "C": [0, 4, 7],
    "Dm": [2, 5, 9],
    "Em": [4, 7, 11],
}

OVERLAP_COUNTS: dict[tuple[str, str], int] = {
    ("C", "C"): 3,
    ("C", "Dm"): 0,
    ("C", "Em"): 2,
    ("Dm", "Dm"): 3,
    ("Dm", "Em"): 0,
    ("Em", "Em"): 3,
}

DISTANCES: dict[tuple[str, str], float] = {
    ("C", "C"): 0.0,
    ("C", "Dm"): 1.0,
    ("C", "Em"): 0.5,
    ("Dm", "Dm"): 0.0,
    ("Dm", "Em"): 1.0,
    ("Em", "Em"): 0.0,
}
