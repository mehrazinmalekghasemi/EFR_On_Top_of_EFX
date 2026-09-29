# Closing the full star and separating the two-source failure cases

Date: 2026-09-27. Four agents, ten goods, nonnegative additive valuations, EFX0.
This continues [DANGEROUS_ITEM_PROGRESS.md](DANGEROUS_ITEM_PROGRESS.md).

**Result:** the complete `1233_248` graph row is excluded as a terminal extremal
obstruction. The previously open sole-champion/later-priority branch has a
Pareto improvement, so no change of priority is needed. The current atlas has
**102 open graph templates: 94 two-source and 8 three-source**.

The four two-source failure types below have separate proved implications and
repair criteria. They do not yet form a universal progress theorem. No overall
EFR counterexample, Mode C counterexample, or universal three-agent theorem is
claimed. No exhaustive valuation campaign was run.

## 1. Setup

Use the notation A_o={a}, A_p=P={h,ell}, A_q=Q, A_r=R, with sizes 1,2,3,3.
For the full-star row, P,Q,R are unenvied and all three owners envy {a}.
Let u_j=v_j(A_j), z_j=v_j(g), and

    R_j(S)=max_{x in S} v_j(S minus {x}),     R_j(empty)=0.

Apply the earlier elementary reductions first: immediate EFR insertion, an
envied pool singleton, a self-pair improvement, a safe-pair source-path
improvement, or pair compensation. If none applies, the conditions E1–E4 in
[DANGEROUS_ITEM_PROGRESS.md](DANGEROUS_ITEM_PROGRESS.md#1-framework-and-elementary-reductions)
hold. In particular:

- z_j<=u_j;
- z_k+v_k(x)<=u_k for x in A_k, k=p,q,r;
- z_o+v_o(x)<=u_o for x in P union Q union R;
- if q champions h in P, then v_p(c)<v_p(h) for every c in Q.

An item x is dangerous to j when z_j+v_j(x)>u_j. Every pair of old items from
P,Q,R, and every pair {g,x} with such an item, is safe at all old utility levels.
Old subbundles are safe too. A Pareto improvement therefore respects any fixed
lexicographic priority, including a priority in which r precedes q.

## 2. The sole champion must enter one of two precise configurations

Assume q is the sole triple owner championing P. This is a role name, not an
agent relabeling or a change in priority. Insertion into P is blocked; o cannot
block it under the source-path cuts, and r cannot block without championing a
pair {g,x}. Thus q blocks and z_q>u_q/2.

The previous proof shows that no Q item is dangerous for p or o. If a triple
replacement at q works, it gives Pareto progress. Otherwise r finds two Q
items dangerous, forcing z_r>u_r/2. Both self-pair bounds imply

    u_q/2<z_q<=2u_q/3,       u_r/2<z_r<=2u_r/3.

There are exactly two r-dangerous Q items, denoted c,c'. If r has a safe triple
replacement, again we are done. Otherwise:

- p finds at most one R item dangerous, since z_p<=u_p/2 and v_p(R)<=u_p;
- q finds at most two R items dangerous, since z_q<=2u_q/3 and v_q(R)<=u_q;
- o finds none, by the source-path cuts.

Consequently only two configurations remain:

(M) q finds two R items dangerous: mutual two-item danger.

(S) q finds exactly one R item d dangerous, and p finds a different item e
of R dangerous: split danger.

If q found none, or if q and p only found the same item dangerous, deleting
that item and inserting g would already be an EFX improvement for r.

## 3. Mutual danger does not need two pair champions

### Lemma M. One pair champion suffices in the mutual-danger configuration

Assume both triples have two dangerous items in the other triple, and q
champions an item h of P. Then there is a Pareto-improving partial EFX allocation.
Only one pair champion is needed.

**Proof.** Every R item is worth less than z_q to q: for any chosen R item,
there is a different q-dangerous item d, and

    v_q(R)<=u_q,       v_q(d)>u_q-z_q.

Every Q item is worth at most u_q-z_q to q by the self-pair bound. Therefore
every mixed Q/R pair is worth less than u_q to q. Symmetrically, every mixed
pair is worth less than u_r to r.

Exchange an r-dangerous c in Q and a q-dangerous d in R. Both owners strictly
improve, and all their EFX comparisons hold. If neither o nor p objects, this
is the required improvement.

Otherwise an external observer j in {o,p} envies a mixed pair E={x,y}, with
x in Q and y in R. **Keep q as the pair champion; do not reorient the roles.**
Choose an r-dangerous c in Q different from x; two such items exist. Set

    C=(R minus {y}) union {c}.

Agent r strictly improves because v_r(c)>u_r-z_r>=v_r(y). Every deletion pair
from C is safe to q by the mixed-pair observation above. It is also safe to j:
unmixed pairs are old source subbundles, and a mixed pair has value at most

    (u_j-v_j(x))+(u_j-v_j(y)) < u_j.

If j=o, give o the pair E, q the singleton {a}, and r the triple C; leave p
unchanged. If j=p, give p the pair E, q the pair {g,h}, and r the triple C;
leave o unchanged. In either case three agents improve, and only the other
external observer k can object to C.

If k does object, its envied deletion pair F in C must be mixed and is disjoint
from E. Give E,F to their respective champions o,p, give {g,h} to q, and give
{a} to r. All four agents strictly improve. Every target is a safe pair or a
singleton, and the goods are disjoint. Thus the result is EFX. QED.

The essential improvement over the earlier D4 proof is to keep the sole pair
champion fixed and use the other triple owner's own remainder in C. The former
need to give {g,h} to either triple owner was a limitation of that construction,
not an impossibility.

## 4. Split danger supplies its own compensation

### Lemma S. Split danger always permits Pareto progress

Use the notation in configuration (S): c,c' are the r-dangerous Q items, d is
the unique q-dangerous R item, and e is the unique p-dangerous R item, d!=e.
Choose h in P championed by q, and let ell be the other P item.

Since z_p<=min(v_p(h),v_p(ell)),

    v_p(e)>u_p-z_p >= max(v_p(h),v_p(ell)).               (1)

Thus e compensates p for giving up h. Propose

    B_p={ell,e},       B_q={g,h},
    B_r=C=(R minus {e}) union {c},       B_o={a}.          (2)

All three changed agents strictly improve: p by (1), q by championship, and r
because v_r(c)>u_r-z_r>=v_r(e).

The only potentially difficult target is C. It is safe to p even at its old
utility: v_p(c)<v_p(h) by failed pair compensation, and every item in R minus
{e} has value less than z_p. Hence every mixed deletion pair is worth less
than v_p(h)+z_p<=u_p; unmixed pairs are old safe subbundles.

If q objects to C at its new utility v_q(g+h), the offending pair must be
{c,d}. Indeed the remaining R item f is not dangerous to q, so

    v_q(c)+v_q(f) <= 2(u_q-z_q) < u_q < v_q(g+h),

and the unmixed R pair is safe. In this event replace (2) by

    B_p={ell,e},       B_q={c,d},       B_r={g,c'},       B_o={a}.

Every changed agent strictly improves; all new targets are safe pairs or a
singleton. This is EFX.

Otherwise q's comparison holds. If o objects to C, it envies a mixed pair
{c,x}, with x in R minus {e}. Give

    B_o={c,x},       B_p={ell,e},       B_q={a},       B_r={g,c'}.

Now every agent strictly improves, and every target is again a safe pair or
singleton. Disjointness uses c!=c' and x!=e. This is EFX.

If neither q nor o objects, (2) itself is the required Pareto improvement.
These alternatives cover every possible comparison. QED.

<a id="t11"></a>
## 5. T11: the full `1233_248` row is excluded

**Theorem.** A nine-good EFX allocation whose sizes are (1,2,3,3), whose three
nonsingleton bundles are sources, and whose three source owners all envy the
singleton has either an EFR insertion or a partial EFX Pareto improvement.

**Proof.** Apply the elementary reductions in Section 1 when available. If
insertion remains blocked, at least one triple owner champions P. If both do,
D4 in the previous note applies. If exactly one does, Section 2 reduces to a
safe triple replacement, mutual danger, or split danger. Lemmas M and S settle
the last two. Every nonterminal move is a Pareto improvement. QED.

This covers every fixed physical priority. Composing with the documented BCFF
restoration theorem rules out the entire graph as a terminal extremal
obstruction. Local moves can release multiple goods. The theorem does not
assert immediate insertion from every starting allocation, a three-agent
bound, universal Mode C, or the distance-five conjecture.

The atlas changes from 103 to 102 open graph templates. Human-proof exclusions
increase from 1,189 to 1,190; the 52 additional computer-checked exclusions are
unchanged. Profile (1,2,3,3) now has 45 open graphs, not 46. The priority-decorated
open catalog has 2,280 representatives: 2,136 two-source and 144 three-source.

## 6. Two-source failure type F1: no eligible champion

This phrase must distinguish two failures.

**A blocked source always has a safe champion.** The minimum-cardinality
envied-subset argument gives T subset of A_s+g, containing g, with |T|<=|A_s|.
Thus absence of *every* safe champion cannot be the obstruction. What may be
missing is a pair champion, a usable predecessor on an envy path, or a donor
compatible with the selected relay.

**Higher-cardinality upgrade.** If s owns a triple and no pair {g,h}, h in A_s,
is envied by any agent, failed insertion guarantees a safe champion triple
{g,h,k}. Every deletion pair is safe: it is either an old pair or an unenvied
{g,h}. The minimum-cardinality argument guarantees an envied triple because
there is no envied singleton or pair and the old source triple is unenvied.

More generally, for a larger source the same argument proceeds by cardinality:
if every smaller subset is unenvied, the first envied subset is automatically
safe. The correct next move class must permit these larger bundles.

**Longer paths.** For an envy path a_0->...->a_k=i disjoint from a donor t,
rotate old bundles along the path and give a safe T subset of A_t+g to i.
Every path agent improves if i champions T. Give t a safe compensation C from
the released goods. Only t's EFX comparisons and the fixed-priority condition
remain to be proved. A path's immediate predecessor may be a singleton;
C1's restriction on a nonsingleton path-start must not be mistaken for absence
of an envy path. A longer path may use four agents.

**Still open:** guaranteeing suitable compensation for one of these higher-
cardinality or longer-path champions. Merely proving a champion exists does
not close a two-source case.

## 7. Two-source failure type F2: an earlier-priority donor

Let G be all strict gainers in the proposed move. A donor preceding the
champion does **not** by itself prevent progress: another path agent may
precede the donor. For example the saved residual escape works with priority
(2,3,0,1): path-start 2 improves before donor 3, although champion 0 is later.

If the donor precedes every member of G and is the only possible loser, it
must weakly recover its old utility u_t. This is necessary, not a choice of
analysis. For a pair relay T={g,h} with compensation from

    H=A_s union (A_t minus {h}),

full recovery is impossible unless

    v_t(A_s) >= v_t(h),                                  (3)

because v_t(H)=u_t-v_t(h)+v_t(A_s). If (3) fails, no choice of compensation
subset, however large, can save **this relay** under this priority.

A proved sufficient repair is to replace h by a compensation item y in A_s.
Write D=A_t minus {h}. If

    v_t(y)>=v_t(h),
    v_j(y)+R_j(D)<=u_j for every j!=t,                    (4)

then C=D+{y} is safe to every other agent at its old utility. Deleting y leaves
an old safe subbundle; deleting an item of D gives exactly the second bound.
The donor recovers, so the resulting eligible relay is a Pareto improvement.
This extends pair compensation to a larger donor remainder.

**Still open:** the guarantee of a y satisfying all observer bounds, or a
different move when the total-value obstruction (3) holds. Priority is never
reset after seeing a failed move.

## 8. Two-source failure type F3: a dominant donated item

For the two-singleton residual relay, if a strict gainer precedes t and the
self-pair bound holds, every champion item with v_t(h)<=u_t/2 is handled by R1.
Therefore failure across all eligible items forces every such champion to be
the donor's unique item with v_t(h)>u_t/2. There can be at most one such item.

This yields a sharper necessary compensation budget. EFX toward the new pair
{g,h} requires the donor's new value to be at least v_t(h). Since every allowed
compensation subset lies in H, even EFX is impossible within this relay unless

    v_t(A_s) >= 2v_t(h)-u_t.                             (5)

This bound allows a later-priority loss. For an earlier donor, (3) is stronger.
Neither bound is sufficient: the compensation bundle must also be safe.

If t is a source, championship by i additionally implies

    v_i(A_t minus {h}) < v_i(g),

because v_i(A_t)<=u_i and v_i(g)+v_i(h)>u_i. This is an explicit inequality
available for a new exchange or compensation argument; it is not a contradiction.

**Still open:** converting these unique-dominant-item configurations into
another move. They are now a more constrained target than arbitrary failures
of the top-two compensation test.

## 9. Two-source failure type F4: another bundle's EFX constraint

Use the enlarged compensation menu from R2: the best safe pair from H, A_s,
and the donor remainder. When the residual covers {g,h}, failure with an
earlier strict gainer forces an old target A_j to satisfy

    R_t(A_j) > M_t >= u_t-v_t(h).

**A two-good blocking target supplies a new repair.** If A_j={b,x}, choose b
with v_t(b)>u_t-v_t(h). Then {h,b} is a safe pair and strictly improves t,
without using g. If some y in A_t minus {h} satisfies v_j(y)>=v_j(b), give

    B_t={h,b},       B_j={x,y},

leaving the other agents unchanged and releasing unused goods. Both targets
are safe pairs; t improves and j does not lose. This is a Pareto-improving EFX
allocation, independent of priority. The proposed original relay can be
abandoned in favor of this move.

If this move is unavailable, it yields the concrete strict inequalities
v_j(y)<v_j(b) for all such y. These are further necessary conditions on a
terminal obstruction, not a counterexample to existence.

**Larger targets.** If the obstructing target is A_i handed to s, trim it to
D subset of A_i while preserving v_s(D)>=u_s. This weakens R_t(D) and releases
A_i minus D for compensation. For safe T and C, the exact remaining donor
threshold becomes

    v_t(C)>=max(R_t(T),R_t(D),R_t(A_r)).

The priority condition must be recomputed: if s was the earlier strict gainer,
trimming must preserve its strict gain unless another earlier gain suffices.
If the unchanged fourth bundle is the obstruction, a four-agent repair may be
needed; no universal trimming/compensation guarantee is currently proved.

## 10. Current conclusions and validation

| Target | Result |
| --- | --- |
| Sole champion, later priority, in `1233_248` | **Solved by Pareto progress** |
| Whole `1233_248` graph row | **T11**; removed from open ledger |
| No eligible pair champion | Safe larger champion exists under the stated blocked-source conditions; repair remains conditional |
| Early donor | Exact recovery necessity (3), sufficient compensation test (4) |
| Dominant donated item | Unique dominant item and exact necessary budget (5) |
| Other EFX target | Proved pool-free repair for a pair target with compensation; trimming criterion for larger targets |
| Universal two-source progress / EFR / Mode C | **Open** |

The eight saved sole-champion examples exercise replacement, mutual-danger
exchange and repairs, and all split-danger branches. Independent set-and-sum
checks verify EFX, disjointness and Pareto improvement under all 24 simultaneous
agent relabelings and reversed triple-role arguments. The universal claim is
supported by the human proof above, not inferred from those examples.

Code: `efr/dangerous_moves.py`; tests: `tests/test_full_star.py`; evidence:
[sole-champion-witnesses.json](../experiment-results/dangerous-items/sole-champion-witnesses.json).

    python -m unittest -v tests.test_full_star
    python -m unittest discover -v
    python -m efr.case_status --check

The next research targets are the eight other three-source stars and the
unique-dominant-item / full-recovery obstructions in the two-source cases.
No completion-time estimate or new exhaustive workflow is claimed.
