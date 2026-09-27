"""Dominant-item compensation and blocker rerouting; no valuation-space search.

See research/DOMINANT_ITEM_OBSTRUCTION.md. A negative result applies only to
this fixed relay and its stated reroutings, never to EFR existence.
"""
from itertools import combinations
from efr.dangerous_moves import _context, _certificate
from efr.compensation import check_priority


def dominant_relay(values, A, g, s, i, t, h, priority=(0, 1, 2, 3)):
    """Try all minimal threshold covers (at most 20) and proved blocker swaps."""
    priority = check_priority(priority)
    rows, items, val, R, u = _context(values, A, g)
    if len({s, i, t}) != 3 or not {s, i, t} <= set(range(4)):
        raise ValueError('Three distinct agents required')
    r = next(j for j in range(4) if j not in {s, i, t})
    if A[i].bit_count() != 1 or A[r].bit_count() != 1:
        raise ValueError('Two singleton targets required')
    if min(A[s].bit_count(), A[t].bit_count()) < 2:
        raise ValueError('Nonsingleton start and donor required')
    if h not in items(A[t]): raise ValueError('h must belong to donor')
    z = [rows[j][g] for j in range(4)]
    if any(z[j] > u[j] for j in range(4)):
        raise ValueError('Pool bound required')
    ht = rows[t][h]
    if 2*ht <= u[t] or ht+z[t] > u[t]:
        raise ValueError('Dominant item and self-pair bound required')
    T = (1 << g) | (1 << h)
    if val(i, T) <= u[i] or val(s, A[i]) < u[s]:
        raise ValueError('Eligible relay required')
    gains = {i} | ({s} if val(s, A[i]) > u[s] else set())
    late = any(priority.index(j) < priority.index(t) for j in gains)
    L = ht if late else u[t]
    H = A[s] | (A[t] ^ (1 << h))
    B = list(A); B[s] = A[i]; B[i] = T
    observers = (s, i, r)
    w = {j: val(j, B[j]) for j in observers}
    subsets = [sum(1 << x for x in xs) for k in range(1, 7)
               for xs in combinations(items(H), k)]
    covers = [C for C in subsets if val(t, C) >= L and
              all(val(t, C ^ (1 << x)) < L for x in items(C))]
    assert len(covers) <= 20
    report = dict(scope='Fixed dominant relay and blocker reroutings only',
                  threshold=str(L), branch='later_loss' if late else 'full_recovery',
                  available_value=str(val(t, H)), minimal_covers=covers,
                  obstructions=[])
    for C in covers:
        if all(R(j, C) <= w[j] for j in observers):
            B[t] = C
            report['move'] = _certificate(rows, A, B, 'dominant_minimal_cover',
                                           priority=priority, compensation=C)
            return report
        # Minimal among subsets envied at ANY observer's provisional utility.
        envied = [E for E in subsets if E != C and E & C == E and
                  any(val(j, E) > w[j] for j in observers)]
        minimal = [E for E in envied if not any(F != E and F & E == F for F in envied)]
        assert minimal
        blockers = []
        for E in minimal:
            for j in observers:
                if val(j, E) <= w[j]: continue
                displaced_value = val(t, B[j])
                if displaced_value >= L:
                    out = list(B); out[t] = B[j]; out[j] = E
                    report['move'] = _certificate(rows, A, out, 'dominant_blocker_rerouting',
                                                   priority=priority, blocker=j,
                                                   compensation=C, envied_subset=E)
                    return report
                blockers.append(dict(agent=j, subset=E,
                                     displaced_value=str(displaced_value)))
        report['obstructions'].append(dict(compensation=C, blockers=blockers))
    report['move'] = None
    return report
