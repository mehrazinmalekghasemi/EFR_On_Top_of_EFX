# Different proof strategies for two and three sources

Date: 2026-09-28 (Tehran). Nonnegative additive 4-agent, 10-good instances;
EFX0 and a fixed physical agent priority throughout.

**Outcome:** enlarging the blocker resolves the latest top-up counterexample.
The three-source analysis instead yields a guarded extension of the triple
exchange proof and an exact forbidden-pair criterion for four-good sources.
No entire open graph is closed: the ledger remains **94 two-source and 8
three-source templates**.

## 1. Split the problem before choosing the move

| Region | Open templates | Appropriate next strategy |
| --- | ---: | --- |
| Two sources, two singleton bundles: (1,1,2,5), (1,1,3,4) | 31 | Jointly enlarge the blocker and compensate the donor |
| Two sources, one singleton: (1,2,2,4), (1,2,3,3) | 63 | Also track the unchanged nonsingleton target's deletion constraint; the two-singleton theorem does not apply directly |
| Three sources: (1,2,3,3) | 4 | Dangerous-item exchanges, with explicit checks on who accepts the singleton |
| Three sources: (1,2,2,4) | 4 | Dangerous-pair intersections for the four-good source |

The 31/63 split matters: the six released goods and four leftover goods in
D12–D15 relied on *two singleton targets*, not merely two sources. Those bounds
must not be applied indiscriminately to all 94 cases.

## 2. Two sources: D16, lift surplus and compensate jointly

Keep the notation of [D14–D15](SINGLETON_BLOCKER_TOP_UP.md): an observer j
receives a minimal envied subset E, and its displaced bundle K_j is offered
to donor t. Let U=H minus E, with |U|<=4. Rather than fixing E and assigning
all chosen leftovers to the donor, partition some of U into disjoint X,F:

    blocker j receives E'=E union X,
    donor t receives Q=K_j union F.

The two other provisional observer bundles stay fixed. The unused part of U
may be released. This increases the blocker's utility by v_j(X), while using
some of the donor's possible compensation. Both changes must be evaluated.

**D16 (exact local criterion).** Let B_k be the three final observer bundles,
W_k=v_k(B_k), and q=max_{k!=t} R_t(B_k). Set L=q when a strict gainer precedes
t, and L=max(q,u_t) otherwise. The allocation is EFX with fixed-priority
progress exactly when:

1. E' is safe to the two other observers at their W levels;
2. Q is safe to all three observers at their W levels;
3. v_t(Q)>=L.

**Proof.** All unchanged observer targets are old safe pairs or singletons.
The only new targets are E' and Q, so (1)–(2) list exactly the observer checks.
Condition (3) combines the donor's remaining EFX comparisons and its required
priority recovery. The old champion remains a strict gainer, and j's enlarged
bundle weakly increases its already strict gain. Disjointness is built into
the partition X,F. QED.

Crucially, enlarging E may make it unsafe to a third agent; condition (1)
cannot be omitted. Nor may the minimal-top-up reduction be used to discard
possible *surplus* goods before the joint split is considered.

There are at most 3^4=81 assignments of U to the blocker, donor, or pool for
each fixed E,j. This is a small exact local routine, not an enumeration of
valuations, and failure does not establish a global obstruction.

### A complete EFX escape from the previous safety counterexample

Recall the example with early donor t=3, deficit 9, leftover donor value 20,
and blocker surplus only 1. Its matrix is

    i: 10 0 6 2 2 4 6 0 0 7
    r:  0 3 0 0 0 0 0 0 0 2
    s:  5 5 1 1 1 0 0 0 0 2
    t:  0 0 6 6 6 18 4 4 4 3.

Start with A=({0},{1},{2,3,4},{5,6,7,8}), g=9 and pi=(3,0,1,2).
Every top-up failed when i was fixed at E={2,6}, worth 12 to i. Instead set

    E'={2,3,6},       Q={4,5,7,8,9},
    B_r={1},         B_s={0}.

The blocker's value rises to 14 and its surplus over {g,h} rises from 1 to 3.
The donor top-up F={4,7,8} is worth 14 to t; R_i(F)=2 now fits the surplus.
The whole donor bundle is worth 35 to t, above its old 30. Its largest deletion
value to i is 13, below i's new 14. The other observers' comparisons also hold.
Thus this is a **complete EFX Pareto improvement**, with utilities

    (10,3,3,30) -> (14,3,5,35).

This resolves that example while preserving the same priority. It does not
prove that every two-source blocker has a suitable joint split.

For the other 63 two-source templates, the same principle of increasing the
blocker utility is plausible, but a proof must additionally retain the large
old-target deletion floors and rederive the available-good count. No claim of
coverage for those 63 templates is made by this implementation.

## 3. Three sources: D17, who actually needs the singleton?

In the four remaining (1,2,3,3) templates, all nonsingleton bundles are sources.
Write A_o={a}, A_p=P (a pair), A_q=Q and A_r=R (triples). The original T11
whole-graph theorem required p,q,r all to envy a. Its non-elementary exchange
constructions, however, assign a only to q or r, never to p.

**D17 (guarded extension).** The constructive full-star kernel still gives a
partial EFX Pareto improvement if only q and r strictly envy a, provided its
explicit guards hold:

- pool bounds z_j<=u_j;
- all three source bundles are unenvied;
- source self-pair cuts z_k+v_k(x)<=u_k for x in A_k;
- singleton-observer cuts z_o+v_o(x)<=u_o for every source item;
- pair compensation is unavailable as in E4;
- insertion into P is blocked by q or r.

**Proof.** Under these hypotheses, the dangerous-item deductions and the
replacement, mutual-danger, and split-danger constructions in T11 are
unchanged. The pair owner either retains P or receives a safe mixed pair or
compensation pair that strictly improves it. Only the triple owners ever
receive a, and they both strictly prefer it. Thus every EFX inequality and
Pareto comparison in the earlier construction remains valid. This also
covers the earlier both-champion construction, whose singleton recipients
are always triple owners. QED.

This covers a continuous guarded subregion of the open graph `1233_240`
(q->o and r->o, with p not envying o), for every fixed priority.
It **does not close that graph**. When p does not envy a, failure of the
singleton-observer cuts on P is no longer automatically removable by the
old p->o path. Insertion into P may also be blocked only by o. These missing
branches must be handled separately.

For `1233_008`, `1233_048`, and `1233_040`, one or both triple owners need not
accept a. The correct next proof obligation is to replace the specific
singleton-dependent fallback, not to assume the extra source makes every
exchange safe. The pair and singleton acceptance conditions remain explicit.

## 4. Three sources: D18, four-good sources have dangerous pairs

Now let B=A_s be an unenvied four-good source, and consider replacing x in B
by g. For each observer j!=s call a pair Y subset B forbidden when

    z_j+v_j(Y)>u_j.

Let F be the union of these forbidden pairs, retaining observer labels.

**D18 (exact replacement criterion).** If z_s>v_s(x), replacing x by g is a
strict Pareto EFX improvement exactly when x belongs to every pair in F.
With no forbidden pair, every profitable replacement works.

**Proof.** Deleting g leaves an old source subbundle, safe to all observers.
Every other deletion leaves g together with a pair Y subset B minus {x}.
All such deletions are safe exactly when no forbidden pair avoids x. The
source owner strictly improves, so all its comparisons against unchanged
old targets remain valid. QED.

If the intersection of all forbidden pairs is empty, the failure has one of
two small certificates:

1. two disjoint forbidden pairs;
2. three forbidden pairs forming a triangle.

**Proof of the certificate claim.** If there is no disjoint pair, all pairs
intersect. Take two distinct pairs {a,b},{a,c}. Empty common intersection
forces a pair not containing a; pairwise intersection then forces {b,c}.
These three form a triangle. Repeated observer labels on the same pair do
not change the argument. QED.

There is a separate utility obstruction: a common item may exist but none
is worth less than g to its owner. Empty pair intersection must not be
confused with this failure of strict improvement.

### Numerical consequences when one observer supplies the obstruction

Unenviedness gives v_j(B)<=u_j. If the same observer j forbids two disjoint
pairs, summing the two strict inequalities yields

    z_j>u_j/2.

If the same observer forbids a triangle, summing its three inequalities and
using nonnegativity yields

    z_j>u_j/3.

For triangles whose edges have different observers, these scalar bounds
cannot be combined across valuation rows; retain the three labeled inequalities.
The singleton blocker can create the entire triangle by itself, even when
all four replacements would strictly improve the source owner.

This gives a focused strategy for the four open (1,2,2,4) templates: handle
profitable common removals first, then analyze disjoint-pair and triangle
certificates, distinguishing single-observer from mixed-observer blockers.
It is a replacement obstruction classification, not a proof that every such
certificate has a broader repair.

## 5. Status and next obligations

| Target | Proved progress | Still needed |
| --- | --- | --- |
| Two sources, two singletons | Exact joint surplus/top-up criterion; previous hard example now has complete EFX Pareto escape | A universal disjunction when every joint split fails |
| Two sources, one singleton | No new universal lemma here | Incorporate the remaining nonsingleton target into surplus repair |
| Three sources, (1,2,3,3) | Guarded kernel extends to non-envying pair owner | Handle singleton-observer pair blocks and unavailable singleton recipients |
| Three sources, (1,2,2,4) | Exact forbidden-pair criterion and two small certificate types | Repair the certificates or obtain EFR insertion |

The most focused next three-source target is `1233_240` outside D17's guards.
For the four-good source, start with a triangle belonging to one observer
before mixing observer labels. For two sources, retain both the donor deficit
and the blocker's surplus as explicit quantities; do not reset priority.

Code: `efr/source_strategies.py` and the relaxed explicit guard in
`efr/dangerous_moves.py`. Evidence and tests verify constructions; the universal
local claims above rest on their proofs, not on sampled valuations.
