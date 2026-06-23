"""
Frozen tests for M3.T1: satisfaction and is_satisfied.
Asserts concrete golden values on the constructed 1D window.
"""
import pytest

from tests.conftest import (
    WINDOW_CHORDS,
    WINDOW_SLOTS,
    WINDOW_TOTAL_SLOTS,
)

# Safe import stubs to guarantee collection when implementation is missing
try:
    from schellingchords.agents import ChordAgent
    from schellingchords.metrics import jaccard_distance
except ImportError:
    class ChordAgent:
        def satisfaction(self, *a, **k): raise NotImplementedError("M3 implementation pending")
        def is_satisfied(self, *a, **k): raise NotImplementedError("M3 implementation pending")
    def jaccard_distance(*a, **k): raise NotImplementedError("M2 implementation pending")


def _get_occupied_neighbors(idx, radius, total_slots):
    """Return list of chord names for occupied neighbors within radius."""
    lo = max(0, idx - radius)
    hi = min(total_slots, idx + radius + 1)
    return [
        WINDOW_CHORDS[n]
        for n in range(lo, hi)
        if n != idx and WINDOW_SLOTS[n] == 1
    ]


@pytest.mark.parametrize(
    "agent_idx, expected_sat, expected_satisfied",
    [
        (2, 1.0, True),   # Surrounded by identical C chords (dist 0.0 <= tol 0.6)
        (8, 0.0, False),  # Surrounded by Bdim chords (dist 0.8 > tol 0.6)
        (14, 1.0, True),  # Only vacant neighbors -> vacuously satisfied
    ],
)
def test_satisfaction_and_is_satisfied(agent_idx, expected_sat, expected_satisfied, window_config):
    """Assert satisfaction fraction and boolean threshold against hand-computed goldens."""
    agent = ChordAgent(unique_id=agent_idx, model=None)
    agent.chord_name = WINDOW_CHORDS[agent_idx]

    neighbors = _get_occupied_neighbors(
        agent_idx, window_config["radius"], WINDOW_TOTAL_SLOTS
    )

    sat = agent.satisfaction(neighbors, jaccard_distance, window_config["tolerance"])
    assert sat == pytest.approx(expected_sat, abs=1e-9)

    is_sat = agent.is_satisfied(
        neighbors, jaccard_distance, window_config["tolerance"], window_config["happiness"]
    )
    assert is_sat is expected_satisfied
