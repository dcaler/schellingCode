"""
Gate test G3: M3 integration.
Validates identical-neighbor satisfaction, tritone-surrounded dissatisfaction,
and correct relocation to the higher-satisfaction empty slot in one pass.
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
        def is_satisfied(self, *a, **k): raise NotImplementedError("M3 implementation pending")
        def desired_slot(self, *a, **k): raise NotImplementedError("M3 implementation pending")
    def jaccard_distance(*a, **k): raise NotImplementedError("M2 implementation pending")


def _get_occupied_neighbors(idx, radius, total_slots):
    lo = max(0, idx - radius)
    hi = min(total_slots, idx + radius + 1)
    return [WINDOW_CHORDS[n] for n in range(lo, hi) if n != idx and WINDOW_SLOTS[n] == 1]


def test_gate_m3_agent_behavior(window_config):
    """
    G3: In a constructed 1D window with real Jaccard metric:
    1. Identical-neighbour agent (C at idx 2) is satisfied.
    2. Tritone-surrounded agent (F at idx 8, neighbors are Bdim) is unsatisfied.
    3. Its desired_slot resolves to the empty slot yielding highest satisfaction (idx 15).
    """
    radius = window_config["radius"]
    tol = window_config["tolerance"]
    hap = window_config["happiness"]

    # 1. Identical neighbor satisfaction
    agent_c = ChordAgent(unique_id=2, model=None)
    agent_c.chord_name = "C"
    neighbors_c = _get_occupied_neighbors(2, radius, WINDOW_TOTAL_SLOTS)
    assert agent_c.is_satisfied(neighbors_c, jaccard_distance, tol, hap), \
        "C surrounded by identical C chords must be satisfied"

    # 2. Tritone-surrounded dissatisfaction
    agent_f = ChordAgent(unique_id=8, model=None)
    agent_f.chord_name = "F"
    neighbors_f = _get_occupied_neighbors(8, radius, WINDOW_TOTAL_SLOTS)
    assert not agent_f.is_satisfied(neighbors_f, jaccard_distance, tol, hap), \
        "F surrounded by Bdim (dist 0.8 > tol 0.6) must be unsatisfied"

    # 3. Relocation to best empty slot
    rng = random.Random(window_config["seed"])
    best_slot = agent_f.desired_slot(
        WINDOW_VACANT_INDICES,
        WINDOW_SLOTS,
        jaccard_distance,
        tol,
        rng,
    )
    assert best_slot == 15, \
        "F must relocate to slot 15 (next to Dm, dist 0.5 <= tol) for max satisfaction"
