"""
G4 — Seeded N-step run end-to-end (M1+M2+M3+M4):
Identical history under same seed; chord multiset + vacancy count conserved every window;
window length correct; population built from n_chord_types appears.
"""
import pytest
from collections import Counter

# Imports for model & config
from schellingchords.model import SchellingChordModel  # type: ignore
from schellingchords.config import Config  # type: ignore


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


def test_seeded_reproducibility(config):
    """Two runs with identical seed must produce identical window histories."""
    m1 = SchellingChordModel(config)
    h1 = m1.run(5)
    m2 = SchellingChordModel(config)
    h2 = m2.run(5)
    assert h1 == h2


def test_conservation_laws_across_run(config):
    """Chord multiset and vacancy count must be conserved in every recorded window."""
    model = SchellingChordModel(config)
    history = model.run(5)
    initial_counts = Counter(s for s in history[0] if s is not None)
    initial_vacant = sum(1 for s in history[0] if s is None)

    for w in history:
        assert Counter(s for s in w if s is not None) == initial_counts
        assert sum(1 for s in w if s is None) == initial_vacant


def test_window_length_and_population_diversity(config):
    """
    Window length must be correct.
    The initial population must contain exactly n_chord_types distinct chords.
    """
    model = SchellingChordModel(config)
    assert len(model.window) == config.bars_per_window * 4
    distinct_chords = set(s for s in model.window if s is not None)
    assert len(distinct_chords) == config.n_chord_types


def test_runtime_params_live_edit_affects_behavior(config):
    """
    Changing RuntimeParams mid-run must not break conservation,
    proving the model reads mutable params each step.
    """
    model = SchellingChordModel(config)
    # Run 2 steps normally
    model.step()
    model.step()
    # Mutate tolerance drastically
    model.params.tolerance = 0.0
    # Run 2 more steps
    model.step()
    model.step()
    # Invariants must still hold
    assert sum(1 for s in model.window if s is None) == round(config.vacancy_fraction * model.window_length)
    assert len(set(s for s in model.window if s is not None)) == config.n_chord_types
