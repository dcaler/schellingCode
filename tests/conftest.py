"""
Shared fixtures and window constants for M3 frozen tests.
1D window: bars_per_window=4 -> 16 beat-slots.
"""
import pytest

WINDOW_TOTAL_SLOTS = 16
# 1 = occupied, 0 = vacant (rest)
# Indices 0-11 occupied, 12 vacant, 13 vacant, 14 occupied, 15 vacant
WINDOW_SLOTS = [1] * 12 + [0, 0, 1, 0]
WINDOW_OCCUPIED_INDICES = list(range(12)) + [14]
WINDOW_VACANT_INDICES = [12, 13, 15]

# Chord assignment per occupied index
WINDOW_CHORDS = {
    0: "C", 1: "C", 2: "C", 3: "C", 4: "C", 5: "C",
    6: "Bdim", 7: "Bdim",
    8: "F",
    9: "Bdim", 10: "Bdim", 11: "Bdim",
    14: "Dm",
}


@pytest.fixture
def window_config():
    """Returns the exact dataclass-compatible config dict for the test window."""
    return {
        "n_chord_types": 5,
        "bars_per_window": 4,
        "vacancy_fraction": len(WINDOW_VACANT_INDICES) / WINDOW_TOTAL_SLOTS,
        "tolerance": 0.6,
        "happiness": 0.5,
        "radius": 2,
        "tempo_bpm": 120,
        "seed": 42,
    }
