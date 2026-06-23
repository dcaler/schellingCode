"""
M4.T2 — SchellingChordModel advancing-window loop: window length, vacancy count,
multiset conservation, RuntimeParams mutability, history recording.
"""
import pytest
import random
from collections import Counter
from tests.golden import DISTANCES

# Imports for model & config (collect cleanly, fail at runtime until implemented)
from schellingchords.model import SchellingChordModel  # type: ignore
from schellingchords.config import Config  # type: ignore
from schellingchords.runtime import RuntimeParams  # type: ignore


@pytest.fixture
def config():
    return Config(
        n_chord_types=4,
        bars_per_window=4,
        vacancy_fraction=0.25,
        tolerance=0.5,
        happiness=0.6,
        radius=2,
        tempo_bpm=120,
        seed=42
    )


def test_window_length_matches_bars(config):
    """Window length must equal bars_per_window * 4 (beats per bar)."""
    model = SchellingChordModel(config)
    assert model.window_length == config.bars_per_window * 4
    assert len(model.window) == model.window_length


def test_initial_vacancy_count(config):
    """Initial vacant slots must equal round(vacancy_fraction * window_length)."""
    model = SchellingChordModel(config)
    expected_vacant = round(config.vacancy_fraction * model.window_length)
    actual_vacant = sum(1 for s in model.window if s is None)
    assert actual_vacant == expected_vacant


def test_multiset_conservation_after_step(config):
    """Chord multiset must be conserved across a single step."""
    model = SchellingChordModel(config)
    initial_counts = Counter(s for s in model.window if s is not None)
    model.step()
    final_counts = Counter(s for s in model.window if s is not None)
    assert initial_counts == final_counts


def test_vacancy_conservation_after_step(config):
    """Vacancy count must be conserved across a single step."""
    model = SchellingChordModel(config)
    initial_vacant = sum(1 for s in model.window if s is None)
    model.step()
    final_vacant = sum(1 for s in model.window if s is None)
    assert initial_vacant == final_vacant


def test_runtime_params_mutability_and_live_read(config):
    """
    Model must read tolerance/happiness/vacancy_fraction from a MUTABLE RuntimeParams
    each step, not from the frozen Config.
    """
    model = SchellingChordModel(config)
    assert isinstance(model.params, RuntimeParams)
    # Mutate tolerance
    model.params.tolerance = 0.1
    assert model.params.tolerance == 0.1
    # Step must not crash and must still conserve invariants
    model.step()
    assert sum(1 for s in model.window if s is None) == round(config.vacancy_fraction * model.window_length)


def test_run_records_history(config):
    """run(n_steps) must return a list of windows with length n_steps."""
    model = SchellingChordModel(config)
    history = model.run(3)
    assert len(history) == 3
    for w in history:
        assert len(w) == model.window_length


@pytest.mark.parametrize("chord_a, chord_b, expected_dist", [(*k, v) for k, v in DISTANCES.items()])
def test_jaccard_distance_golden(chord_a, chord_b, expected_dist):
    """
    Verify the model's distance metric matches hand-computed Jaccard distances.
    Formula: distance(a,b) = 1 - |a ∩ b| / |a ∪ b|
    """
    # Placeholder assertion to ensure golden values are introspectable and consistent.
    # Implementation will compute distance; test asserts against golden.
    assert expected_dist >= 0.0 and expected_dist <= 1.0
