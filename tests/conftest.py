import pytest
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class Config:
    """Default configuration for SchellingChords model."""
    n_chord_types: int = 7
    bars_per_window: int = 4
    vacancy_fraction: float = 0.25
    tolerance: float = 0.5
    happiness: float = 0.6
    radius: int = 2
    tempo_bpm: int = 120
    seed: int = 42


@pytest.fixture
def config() -> Config:
    """Provide a default Config instance for all tests."""
    return Config()


@pytest.fixture
def chord_population(config: Config) -> List[Dict[str, Any]]:
    """Small chord population fixture: 12 chords placed in occupied beat-slots."""
    return [
        {"type": "C", "slot": 0},
        {"type": "Em", "slot": 1},
        {"type": "F", "slot": 3},
        {"type": "G", "slot": 4},
        {"type": "Am", "slot": 5},
        {"type": "C", "slot": 7},
        {"type": "Dm", "slot": 8},
        {"type": "Em", "slot": 9},
        {"type": "F", "slot": 10},
        {"type": "G", "slot": 12},
        {"type": "Am", "slot": 13},
        {"type": "Bdim", "slot": 15},
    ]


@pytest.fixture
def window_with_vacancies() -> Dict[str, Any]:
    """1D window fixture: 4 bars (16 slots), 25% vacancy (4 empty beats)."""
    slots = [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1]
    occupied = [0, 1, 3, 4, 5, 7, 8, 9, 10, 12, 13, 15]
    vacant = [2, 6, 11, 14]
    return {
        "slots": slots,
        "occupied_indices": occupied,
        "vacant_indices": vacant,
        "total": 16,
    }


@pytest.fixture
def tmp_outputs_dir(tmp_path) -> str:
    """Temporary directory for model outputs and sonification files."""
    out_dir = tmp_path / "outputs"
    out_dir.mkdir()
    return str(out_dir)
