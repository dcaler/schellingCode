# tests/gate_run.py
# G7: CLI `single` on configs/default.yaml produces .mid and .csv in tmp outputs dir;
# `sweep` over tolerance returns one summary row per value.

import csv
import sys
import pytest
from pathlib import Path
from schellingchords.run import main


@pytest.fixture
def default_cfg(tmp_path):
    """Simulate project root with configs/default.yaml."""
    cfg_dir = tmp_path / "configs"
    cfg_dir.mkdir()
    cfg = cfg_dir / "default.yaml"
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


def test_gate_single_cli(default_cfg, tmp_path, monkeypatch):
    """G7: CLI single command produces .mid and .csv in tmp outputs dir."""
    out_dir = tmp_path / "outputs"
    out_dir.mkdir()
    monkeypatch.setattr(sys, "argv", ["run", "single", str(default_cfg), "-o", str(out_dir)])
    main()

    assert any(out_dir.glob("*.mid")), "Gate G7: single CLI must produce .mid"
    assert any(out_dir.glob("*.csv")), "Gate G7: single CLI must produce .csv"


def test_gate_sweep_cli(default_cfg, tmp_path, monkeypatch):
    """G7: CLI sweep over tolerance returns one summary row per value."""
    out_dir = tmp_path / "sweep_outputs"
    out_dir.mkdir()
    monkeypatch.setattr(sys, "argv", [
        "run", "sweep", str(default_cfg), "tolerance", "0.3", "0.5", "0.7", "-o", str(out_dir)
    ])
    main()

    csv_files = list(out_dir.glob("*.csv"))
    assert len(csv_files) == 1, "Gate G7: sweep CLI must produce exactly one summary CSV"
    with open(csv_files[0]) as f:
        rows = list(csv.DictReader(f))
        assert len(rows) == 3, "Gate G7: sweep CLI must return one summary row per value"
        for row in rows:
            assert "tolerance" in row
            assert float(row["tolerance"]) in (0.3, 0.5, 0.7)
