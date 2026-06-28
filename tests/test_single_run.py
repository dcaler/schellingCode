# tests/test_single_run.py
# M7.T1: single() run -> outputs .mid, .csv into outputs/ using dated naming.
# Validates 1D window constraints and config dataclass fields.

import csv
import re
import pytest
from pathlib import Path
from tests.golden import (
    DIATONIC_CHORDS, OVERLAP_COUNTS, DISTANCES,
    WINDOW_TOTAL_SLOTS, WINDOW_SLOTS, WINDOW_OCCUPIED_SLOTS, WINDOW_OCCUPIED_INDICES
)

# Import target module; will fail at execution if unimplemented, but collects cleanly.
from schellingchords.run import single


@pytest.fixture
def tmp_config(tmp_path):
    """Create a minimal valid config matching the required dataclass fields."""
    cfg = tmp_path / "test_config.yaml"
    cfg.write_text(
        "n_chord_types: 3\n"
        "bars_per_window: 4\n"
        "vacancy_fraction: 0.25\n"
        "tolerance: 0.5\n"
        "happiness: 0.6\n"
        "radius: 2\n"
        "tempo_bpm: 120\n"
        "seed: 42\n"
    )
    return cfg


def test_golden_constants_integrity():
    """Verify golden values are internally consistent before model runs."""
    # Freeze reconcile (Cale+Claude): DIATONIC_CHORDS is the full diatonic-major
    # vocabulary constant (7 chords: C, Dm, Em, F, G, Am, Bdim). The original `== 3`
    # was the fixture's n_chord_types (a RUN parameter: how many types to select for
    # a run), mistakenly asserted against the table's structural size. No run.py can
    # change a constant's length, so `== 3` was unsatisfiable (it burned all 4 M7.T1
    # attempts, escalation included). Assert the vocabulary size: 7.
    assert len(DIATONIC_CHORDS) == 7
    for name, pcs in DIATONIC_CHORDS.items():
        assert pcs == sorted(pcs), f"Chord {name} pitch classes must be sorted"
        assert all(0 <= pc <= 11 for pc in pcs), "Pitch classes must be in 0..11"

    assert WINDOW_TOTAL_SLOTS == len(WINDOW_SLOTS)
    assert WINDOW_OCCUPIED_SLOTS == len(WINDOW_OCCUPIED_INDICES)
    assert WINDOW_OCCUPIED_SLOTS + WINDOW_SLOTS.count(0) == WINDOW_TOTAL_SLOTS
    assert all(idx in range(WINDOW_TOTAL_SLOTS) for idx in WINDOW_OCCUPIED_INDICES)


def test_single_run_produces_mid_and_csv(tmp_config, tmp_path):
    """M7.T1: single(config_path) writes per-window MIDI and observables CSV."""
    out_dir = tmp_path / "outputs"
    out_dir.mkdir()
    single(str(tmp_config), str(out_dir))

    mid_files = list(out_dir.glob("*.mid"))
    csv_files = list(out_dir.glob("*.csv"))

    assert len(mid_files) >= 1, "Expected at least one .mid file in outputs/"
    assert len(csv_files) >= 1, "Expected at least one .csv file in outputs/"

    # Freeze reconcile (Cale+Claude): enforce the dated naming the spec requires
    # ({YYMMDD}_{project}_...). The original test only globbed *.mid/*.csv and so
    # silently accepted undated names (window_1.mid / observables.csv); assert a
    # 6-digit YYMMDD_ prefix on every output so that gap cannot recur.
    for f in mid_files + csv_files:
        assert re.match(r"\d{6}_", f.name), \
            f"output {f.name!r} lacks the dated YYMMDD_ prefix"

    # Validate CSV structure matches observables schema
    with open(csv_files[0]) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) > 0, "Observables CSV must contain data rows"
        assert "step" in rows[0], "CSV must track simulation step"
        assert "happy_agents" in rows[0], "CSV must track happy agent count"
        # 1D constraint: no row/col or grid metrics should appear
        for col in rows[0].keys():
            assert "row" not in col.lower() and "col" not in col.lower(), \
                "1D model must not expose 2D grid coordinates"
