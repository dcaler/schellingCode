# tests/test_sweep_cli.py
# M7.T2: sweep() + argparse CLI -> summary CSV with one row per parameter value.

import csv
import pytest
from pathlib import Path
from schellingchords.run import sweep


@pytest.fixture
def tmp_config(tmp_path):
    cfg = tmp_path / "sweep_config.yaml"
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


def test_sweep_produces_summary_csv(tmp_config, tmp_path):
    """sweep(config_path, param, values) writes a phase-diagram summary CSV."""
    out_dir = tmp_path / "sweep_outputs"
    out_dir.mkdir()
    values = [0.3, 0.5, 0.7]
    sweep(str(tmp_config), "tolerance", values, str(out_dir))

    csv_files = list(out_dir.glob("*.csv"))
    assert len(csv_files) == 1, "Sweep must produce exactly one summary CSV"

    with open(csv_files[0]) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == len(values), "Expected one row per sweep value"
        for row in rows:
            assert "tolerance" in row, "Summary CSV must contain the swept parameter column"
            assert float(row["tolerance"]) in values, "Row value must match input sweep values"


@pytest.mark.parametrize("param_name,values,expected_rows", [
    ("tolerance", [0.2, 0.4], 2),
    ("radius", [1, 2, 3], 3),
])
def test_sweep_parametrized(tmp_config, tmp_path, param_name, values, expected_rows):
    """Parametrized sweep validation: arity matches value rows."""
    out_dir = tmp_path / "param_sweep"
    out_dir.mkdir()
    sweep(str(tmp_config), param_name, values, str(out_dir))

    csv_files = list(out_dir.glob("*.csv"))
    assert len(csv_files) == 1
    with open(csv_files[0]) as f:
        rows = list(csv.DictReader(f))
        assert len(rows) == expected_rows, f"Expected {expected_rows} rows for {param_name} sweep"
        for row in rows:
            assert param_name in row, f"CSV must contain {param_name} column"
