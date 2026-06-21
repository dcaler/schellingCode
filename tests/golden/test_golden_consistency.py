"""
Internal-consistency guard for the FROZEN golden values (build infrastructure).

These checks are IMPLEMENTATION-INDEPENDENT: they assert that the frozen golden
constants agree with each other and with objective ground truth (overlap counts vs
actual set intersections; window counts vs the 1D slot list vs the index lists). So they
PASS at Phase 0 with no implementation, and FAIL LOUDLY if the golden module is
internally contradictory — which would otherwise silently make a downstream module
unsatisfiable (the impl can't edit a frozen test, so a wrong golden value = a hard,
unfixable block). Discovered by introspection so it survives qwen restructuring the
module or switching the distance metric; a non-vacuous run is enforced via `checks`.

Not part of any module's behavioral contract — added deliberately to catch bad freezes.
"""
from __future__ import annotations

import tests.golden as G


def test_overlap_counts_are_true_intersections():
    """Every frozen overlap count must equal the real |a ∩ b| of the pitch-class sets."""
    chords = getattr(G, "DIATONIC_CHORDS", None)
    counts = getattr(G, "OVERLAP_COUNTS", None)
    if not chords or not counts:
        return  # nothing of this shape to validate here
    checks = 0
    for (a, b), n in counts.items():
        assert a in chords and b in chords, f"OVERLAP_COUNTS references unknown chord {a!r}/{b!r}"
        true_overlap = len(set(chords[a]) & set(chords[b]))
        assert n == true_overlap, f"OVERLAP_COUNTS[{a},{b}]={n} but |{a}∩{b}|={true_overlap}"
        checks += 1
    assert checks > 0, "OVERLAP_COUNTS present but empty"


def test_distances_consistent_and_in_range():
    """Distances must be in [0,1], agree across the DISTANCES/DISTANCES_EXACT tables,
    and hit the metric-agnostic endpoints (disjoint -> 1, identical -> 0)."""
    chords = getattr(G, "DIATONIC_CHORDS", None)
    exact = getattr(G, "DISTANCES_EXACT", None) or getattr(G, "DISTANCES", None)
    if not chords or not exact:
        return
    checks = 0
    for (a, b), d in exact.items():
        assert 0.0 <= d <= 1.0, f"distance({a},{b})={d} out of [0,1]"
        overlap = len(set(chords[a]) & set(chords[b]))
        if overlap == 0:
            assert d == 1.0, f"disjoint {a},{b} must have distance 1.0, got {d}"
        if set(chords[a]) == set(chords[b]):
            assert d == 0.0, f"identical {a},{b} must have distance 0.0, got {d}"
        checks += 1
    # the two distance tables, if both present, must agree
    d1, d2 = getattr(G, "DISTANCES", None), getattr(G, "DISTANCES_EXACT", None)
    if d1 and d2:
        assert set(d1) == set(d2), "DISTANCES and DISTANCES_EXACT have different key sets"
        for k in d1:
            assert abs(d1[k] - d2[k]) < 1e-9, f"DISTANCES vs DISTANCES_EXACT disagree at {k}"
            checks += 1
    assert checks > 0, "distance tables present but empty"


def test_window_counts_match_slots_and_indices():
    """SchellingChords is ONE-DIMENSIONAL: the window is a flat WINDOW_SLOTS list (0/1 per
    beat), and a beat-slot is addressed by ONE integer index. The occupied/vacant count
    constants and index lists must match the slots; each index must actually be an
    occupied/vacant beat. (Rejects a 2D-grid framing of the window.)"""
    slots = getattr(G, "WINDOW_SLOTS", None)
    if slots is None:
        return
    assert all(s in (0, 1, True, False) for s in slots), \
        "WINDOW_SLOTS must be a FLAT list of 0/1 per beat (1D) — not a 2D grid of rows"
    total = len(slots)
    occ = sum(1 for s in slots if s)
    vac = total - occ
    checks = 0

    def check(name, expected):
        nonlocal checks
        if hasattr(G, name):
            assert getattr(G, name) == expected, f"{name}={getattr(G, name)} but slots say {expected}"
            checks += 1

    check("WINDOW_TOTAL_SLOTS", total)
    check("WINDOW_OCCUPIED_SLOTS", occ)
    check("WINDOW_VACANT_SLOTS", vac)

    occ_idx = getattr(G, "WINDOW_OCCUPIED_INDICES", None)
    vac_idx = getattr(G, "WINDOW_VACANT_INDICES", None)
    if occ_idx is not None:
        assert len(occ_idx) == occ, f"OCCUPIED_INDICES has {len(occ_idx)}, slots have {occ} occupied"
        for i in occ_idx:
            assert slots[i], f"OCCUPIED index {i} is vacant in WINDOW_SLOTS"
        checks += 1
    if vac_idx is not None:
        assert len(vac_idx) == vac, f"VACANT_INDICES has {len(vac_idx)}, slots have {vac} vacant"
        for i in vac_idx:
            assert not slots[i], f"VACANT index {i} is occupied in WINDOW_SLOTS"
        checks += 1
    if occ_idx is not None and vac_idx is not None:
        assert not (set(occ_idx) & set(vac_idx)), \
            "an index is listed as BOTH occupied and vacant"
        checks += 1

    assert checks > 0, "WINDOW_SLOTS present but no count/index constants to validate"
