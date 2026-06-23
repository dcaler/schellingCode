import pytest
from schellingchords.metrics.protocol import DistanceMetric
from schellingchords.metrics.registry import METRICS, get_metric
from schellingchords.metrics.stubs import TymoczkoVoiceLeading, TIV


def test_distance_metric_protocol_defined():
    """M2.T1: DistanceMetric protocol must define distance(a, b) -> float"""
    assert hasattr(DistanceMetric, "distance")


def test_registry_contains_pitch_class_overlap():
    """M2.T1: METRICS registry must contain the default metric"""
    assert "pitch_class_overlap" in METRICS


def test_get_metric_returns_instance():
    """M2.T1: get_metric must return a registered DistanceMetric instance"""
    metric = get_metric("pitch_class_overlap")
    assert metric is not None
    assert isinstance(metric, DistanceMetric)


def test_get_metric_unknown_raises_key_error():
    """M2.T1: get_metric must raise KeyError for unregistered names"""
    with pytest.raises(KeyError):
        get_metric("nonexistent_metric")


def test_tymoczko_stub_raises_not_implemented():
    """M2.T1: TymoczkoVoiceLeading stub must raise NotImplementedError"""
    stub = TymoczkoVoiceLeading()
    with pytest.raises(NotImplementedError):
        stub.distance([0, 2, 4], [1, 4, 6])


def test_tiv_stub_raises_not_implemented():
    """M2.T1: TIV stub must raise NotImplementedError"""
    stub = TIV()
    with pytest.raises(NotImplementedError):
        stub.distance([0, 2, 4], [1, 4, 6])
