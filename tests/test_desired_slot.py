"""
Frozen tests for M3.T2: desired_slot selection.
Asserts best-improving empty slot selection and deterministic tie-breaking.
"""
import random
import pytest

from tests.conftest import (
    WINDOW_CHORDS,
    WINDOW_SLOTS,
    WINDOW_VACANT_INDICES,
    WINDOW_TOTAL_SLOTS,
)

try:
    from schellingchords.agents import ChordAgent
    from schellingchords.metrics import jaccard_distance
except ImportError:
    class ChordAgent:
        def desired_slot(self, *a, **k): raise NotImplementedError("M3 implementation pending")
    def jaccard_distance(*a, **k): raise NotImplementedError("M2 implementation pending")


def test_desired_slot_selects_max_satisfaction():
    """
    F at idx 8 is surrounded by Bdim (dist 0.8 > tol 0.6) -> sat 0.0.
    Moving to 12 yields sat 1/3 ≈ 0.333
    Moving to 13 yields sat 1/2 = 0.5
    Moving to 15 yields sat 1/1 = 1.0 (next to Dm, dist 0.5 <= tol)
    Expected best: 15
    """
    agent = ChordAgent(unique_id=8, model=None)
    agent.chord_name = "F"

    rng = random.Random(42)
    best = agent.desired_slot(
        WINDOW_VACANT_INDICES,
        WINDOW_SLOTS,
        jaccard_distance,
        0.6,
        rng,
    )
    assert best == 15


def test_desired_slot_deterministic_under_seed():
    """Calling desired_slot twice with identical seed must return identical slot."""
    agent = ChordAgent(unique_id=8, model=None)
    agent.chord_name = "F"

    seed = 123
    rng1 = random.Random(seed)
    rng2 = random.Random(seed)

    slot1 = agent.desired_slot(WINDOW_VACANT_INDICES, WINDOW_SLOTS, jaccard_distance, 0.6, rng1)
    slot2 = agent.desired_slot(WINDOW_VACANT_INDICES, WINDOW_SLOTS, jaccard_distance, 0.6, rng2)

    assert slot1 == slot2
    assert slot1 in WINDOW_VACANT_INDICES
