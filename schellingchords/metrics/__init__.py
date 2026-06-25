"""Metrics package for SchellingChords.

Provides distance functions used to compare chord similarity.
"""

from schellingchords.chords import diatonic_major
from schellingchords.metrics.pitch_class_overlap import PitchClassOverlap

# Name -> pitch-class set, sourced from the product chord vocabulary (not test
# goldens) so the function and the vocabulary cannot drift apart.
_PITCH_CLASSES = {c.name: set(c.pitch_classes) for c in diatonic_major()}
_METRIC = PitchClassOverlap()


def jaccard_distance(a: str, b: str) -> float:
    """Jaccard distance between two chords identified by name.

    Looks up each chord's pitch-class set and delegates to the single-source
    :class:`PitchClassOverlap` metric: ``1 - |A ∩ B| / |A ∪ B|``. Identical
    chords -> 0.0; disjoint pitch-class sets -> 1.0. This is the real graded
    metric (e.g. ``F``/``Bdim`` -> 0.8), not a binary same/different.

    Args:
        a: First chord name (e.g. ``"C"``, ``"Bdim"``).
        b: Second chord name.

    Returns:
        Distance in [0.0, 1.0].

    Raises:
        KeyError: if either name is not in the diatonic vocabulary.
    """
    return _METRIC.distance(_PITCH_CLASSES[a], _PITCH_CLASSES[b])
