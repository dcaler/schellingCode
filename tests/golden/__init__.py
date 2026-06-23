"""
Golden constants for SchellingChords M1/M2/M3 consistency guards.
All values are hand-computed and frozen. Implementation must satisfy these.
"""

# Diatonic pitch-class sets (sorted, 0=C, 1=C#, ..., 11=B)
DIATONIC_CHORDS: dict[str, list[int]] = {
    "C":   [0, 4, 7],
    "Dm":  [2, 5, 9],
    "F":   [0, 5, 9],
    "G":   [2, 7, 10],
    "Bdim":[2, 5, 10],
}

# Intersection sizes |a ∩ b| for selected pairs
OVERLAP_COUNTS: dict[tuple[str, str], int] = {
    ("C", "F"): 1,
    ("C", "G"): 1,
    ("F", "Bdim"): 1,
    ("G", "Bdim"): 2,
    ("C", "Bdim"): 0,
    ("F", "Dm"): 2,
}

# Jaccard distance: distance(a, b) = 1 - |a ∩ b| / |a ∪ b|
# Normalised to [0, 1]. Identical -> 0.0, Disjoint -> 1.0.
# Hand-computed examples:
#   C & F: 1 - 1/5 = 0.8
#   F & Bdim: 1 - 1/5 = 0.8
#   F & Dm: 1 - 2/4 = 0.5
#   C & Bdim: 1 - 0/6 = 1.0
DISTANCES: dict[tuple[str, str], float] = {
    ("C", "F"): 0.8,
    ("C", "G"): 0.8,
    ("F", "Bdim"): 0.8,
    ("G", "Bdim"): 0.5,
    ("C", "Bdim"): 1.0,
    ("F", "Dm"): 0.5,
}
