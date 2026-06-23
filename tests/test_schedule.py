"""
M4.T1 — Schedule policy: pure relocation, deterministic collision resolution,
vacancy conservation. No Mesa coupling.
"""
import pytest
import random
from collections import Counter

# Import schedule policy (will fail at runtime until implemented, but collects cleanly)
from schellingchords.schedule import apply_relocation_policy  # type: ignore


@pytest.fixture
def rng():
    return random.Random(123)


@pytest.fixture
def base_window():
    """1D window of 8 slots, 4 vacant (indices 2,3,6,7)."""
    return ["C", "Dm", None, None, "Em", "F", None, None]


def test_vacancy_count_preserved(base_window, rng):
    """Relocation must not change the number of empty slots."""
    relocating = [0, 1]
    targets = [2, 3]
    n_vacant = 4
    new_window = apply_relocation_policy(base_window, relocating, targets, rng, n_vacant)
    assert sum(1 for s in new_window if s is None) == n_vacant


def test_deterministic_collision_resolution(base_window, rng):
    """
    When multiple agents target the same vacant slot, resolution must be deterministic.
    Expected rule: process relocating agents in ascending index order.
    If a target is already taken, assign the next available vacant slot in ascending order.
    """
    relocating = [0, 1]
    targets = [2, 2]  # Both want slot 2
    n_vacant = 4
    new_window = apply_relocation_policy(base_window, relocating, targets, rng, n_vacant)

    # Agent at 0 gets slot 2. Agent at 1 gets next available: slot 3.
    assert new_window[2] == "C"
    assert new_window[3] == "Dm"
    assert new_window[0] is None
    assert new_window[1] is None
    assert new_window[4] == "Em"
    assert new_window[5] == "F"
    assert new_window[6] is None
    assert new_window[7] is None


def test_multiset_conservation_during_relocation(base_window, rng):
    """The multiset of chord types must remain identical after relocation."""
    relocating = [0, 4]
    targets = [6, 7]
    n_vacant = 4
    initial_counts = Counter(s for s in base_window if s is not None)
    new_window = apply_relocation_policy(base_window, relocating, targets, rng, n_vacant)
    final_counts = Counter(s for s in new_window if s is not None)
    assert initial_counts == final_counts


@pytest.mark.parametrize("relocating, targets, expected_occupied", [
    ([0], [2], [2]),
    ([1], [3], [3]),
    ([0, 1], [6, 7], [6, 7]),
    ([4, 5], [2, 3], [2, 3]),
])
def test_target_assignment_correctness(base_window, rng, relocating, targets, expected_occupied):
    """Verify agents land exactly on requested vacant slots when no collisions occur."""
    n_vacant = 4
    new_window = apply_relocation_policy(base_window, relocating, targets, rng, n_vacant)
    for idx in expected_occupied:
        assert new_window[idx] is not None
    for idx in relocating:
        assert new_window[idx] is None
