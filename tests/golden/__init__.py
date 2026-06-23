# tests/golden/__init__.py
# Frozen golden values for SchellingChords M7.
# All values are hand-computed, internally consistent, and 1D-aware.

# Diatonic triads in C major (pitch classes 0..11, sorted)
DIATONIC_CHORDS = {
    "C": [0, 4, 7],
    "F": [0, 5, 9],
    "G": [2, 7, 11],
}

# Intersection sizes |A ∩ B|
OVERLAP_COUNTS = {
    ("C", "F"): 1,
    ("C", "G"): 1,
    ("F", "G"): 0,
}

# Jaccard distance: 1 - |A ∩ B| / |A ∪ B|
# C∪F={0,4,5,7,9} (5), C∩F={0} (1) -> 1 - 1/5 = 0.8
# C∪G={0,2,4,7,11} (5), C∩G={7} (1) -> 1 - 1/5 = 0.8
# F∪G={0,2,5,7,9,11} (6), F∩G={} (0) -> 1 - 0/6 = 1.0
DISTANCES = {
    ("C", "F"): 0.8,
    ("C", "G"): 0.8,
    ("F", "G"): 1.0,
}

# 1D Window fixture constants (bars_per_window=4, vacancy_fraction=0.25)
# The Schelling space is a single row of beat-slots. No width/height/grid.
WINDOW_TOTAL_SLOTS = 16  # 4 bars * 4 beats/bar
WINDOW_VACANT_SLOTS = 4  # 16 * 0.25
WINDOW_OCCUPIED_SLOTS = 12  # 16 - 4
WINDOW_SLOTS = [1] * 12 + [0] * 4  # flat list: 1=occupied chord, 0=vacant/rest
WINDOW_OCCUPIED_INDICES = list(range(12))  # integer indices of occupied beats
