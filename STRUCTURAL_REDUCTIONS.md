# Rigorous reductions before an exhaustive EFR search

## What is counted, and what is not

These reductions concern a hypothetical extremal obstruction to **unrestricted
EFR existence**. They are not safe deletions from the existing Mode C point
oracle, which must still consider all possible EFX predecessors and omitted
goods. The old campaign's 220 valuation-ranking roots are a different partition
of the domain; we have not certified that any specified number of those roots
can be removed by these lemmas.

There are 18 nondecreasing four-bundle size profiles summing to nine. Twelve
have an empty bundle, which accepts insertion immediately. The six nonempty
profiles are listed below. For each, enumerate directed acyclic envy graphs
modulo permutations of agents with equal bundle sizes. This gives 1344
**combinatorial templates**, not 1344 equally difficult or necessarily nonempty
valuation regions. Each template still represents an infinite continuous domain.

| Starting sizes | Acyclic templates | After unique-source lemma | After excluding singleton sources | Final templates |
| --- | ---: | ---: | ---: | ---: |
| (1,1,1,6) | 104 | 46 | 0 | 0 |
| (1,1,2,5) | 284 | 121 | 18 | 18 |
| (1,1,3,4) | 284 | 121 | 18 | 18 |
| (1,2,2,4) | 284 | 121 | 57 | 39 |
| (1,2,3,3) | 284 | 121 | 57 | 57 |
| (2,2,2,3) | 104 | 46 | 46 | 24 |
| **Total** | **1344** | **576** | **196** | **156** |

The final reduction removes 1188/1344 = 88.39% of these templates. Of the 156
remaining, 140 have two sources, 15 have three, and one has four. The nonempty
profile (1,1,1,6) is eliminated completely, leaving five size profiles.

For an additional check independent of bundle sizes, the 543 labeled DAGs on
four vertices split by source count as 316,198,28,1. Their unlabeled counts are
16,11,3,1. The exact enumeration and size-preserving group action are implemented
in `structural_reductions.py`. We do not independently relabel a graph and its
bundle sizes.

## Why it suffices to study extremal states

Fix a generic positive additive instance and a fixed ordering of agents. Maximize
the lexicographic tuple of own utilities over all partial EFX allocations. There
are finitely many such allocations. By BCFF's progress theorem, an extremal
allocation has at most one unallocated good. If it is complete, EFR already
exists. Otherwise exactly nine goods are allocated.

A strict envy cycle would give a Pareto improvement, contradicting extremality.
The unique-source progress lemma in RESTORATION_LEMMAS.md also rules out a blocked
extremal allocation having exactly one source. All Pareto improvements below
contradict the same extremality; if a move releases multiple goods, BCFF restores
nine or ten allocated goods with higher fixed lexicographic potential.

This reduction also suffices for arbitrary nonnegative valuations. If an instance
had no EFR allocation, then every one of the finitely many complete allocations
would have a strictly violated EFR inequality. All these chosen strict violations
survive a sufficiently small positive generic perturbation. Hence a counterexample
would imply a positive generic counterexample. Independently normalizing positive
rows does not affect fairness or the relevant comparisons.

The solver uses nonnegative normalized rows, which cover a superset of the generic
cases required by this argument. It does not need to encode nondegeneracy itself.

## Lemma 1: the omitted good cannot be envied at an extremal state

Write u_i=v_i(A_i). If v_i(g)>u_i, replace agent i's bundle by the singleton {g}
and release the old bundle to the pool. Agent i strictly improves; other agents
are unchanged. EFX is preserved because the only new target is a singleton.
Thus an extremal state necessarily satisfies

    v_i(g) <= u_i, for every i.                         (1)

This is a standard elementary pool-envy improvement. It is valid even when i is
not a source, a case our earlier source-only move diagnostic did not enumerate.

## Lemma 2: every source in a blocked extremal state has at least two goods

Suppose source k has A_k={h}. If agent i blocks insertion there, then

    2u_i < v_i(h)+v_i(g),       v_i(h) <= u_i,

where the second inequality uses that k is unenvied. Hence v_i(g)>u_i,
contradicting (1). Equivalently, this gives a concrete improving move by Lemma 1.

No reachability assumption is needed. This strengthens the earlier singleton
source lemma. In (1,1,1,6), at least two sources would force a singleton source,
so that entire extremal size profile can be discarded.

## Lemma 3: a two-good bundle containing g is automatically safe

Assume A is EFX and (1) holds. Let h belong to an old bundle A_k with |A_k|>=2.
For every observer j, v_j(h)<=u_j. For j=k this is nonnegativity. For j!=k,
remove a different good from A_k and apply EFX; the remainder still contains h.
Together with (1), this implies that every one-good deletion from {g,h} is worth
at most u_j to every observer j. Thus {g,h} is safe for all EFX comparisons.

If agent i can be reached from k along an envy path and

    v_i(g)+v_i(h) > u_i,

rotate the path and give {g,h} to i. This is a Pareto-improving partial EFX
allocation. Therefore every extremal state satisfies the **linear** inequalities

    v_i(g)+v_i(h) <= u_i
    whenever |A_k|>=2, h in A_k, and k reaches i.       (2)

Reachability includes the zero-length path i=k. In particular,

    v_i(g) <= u_i - max_{h in A_i} v_i(h), if |A_i|>=2.

For a two-good own bundle this gives

    v_i(g) <= min_{h in A_i} v_i(h) <= u_i/2.          (3)

This is both a theoretical reduction and an encoding simplification: a family
of disjunctive safe-champion tests becomes linear constraints. Only candidate
champion sets of at least three goods need the remaining general disjunctions.

## Lemma 4: who can block a two-good source?

Let source k have two goods. An observer i with a two-good own bundle cannot
block insertion: because k is unenvied and (3) holds,

    v_i(A_k)<=u_i,        v_i(g)<=u_i/2,

so 2(v_i(A_k)+v_i(g))<=3u_i.

Moreover, NO reachable observer can block k at an extremal state. If i blocks,
then u_i < (2/3)v_i(A_k+g). Removing an i-least-valued good leaves an envied pair.
That pair cannot be A_k, since k is unenvied. It is {g,h} for some h in A_k.
By Lemma 3 it is safe; if i is reachable from k, the path rotation improves EFX.
Here exactly nine goods stay allocated, since a two-good source is replaced by
a two-good champion bundle.

Consequently every two-good source in a blocked extremal state needs a blocker
that is BOTH unreachable from it and owns a bundle of size different from two.
If the graph has no such agent, the entire structural template is impossible.
This yields the final 156-template catalog. It also allows insertion-failure
clauses for two-good sources to mention only these remaining candidate blockers.

A useful special case: in profile (2,2,2,3), the only possible blocker of a
pair-source is the three-good agent. If that agent were not a source, some pair
source would reach it, giving the forbidden improvement. Thus the three-good
agent must be a source. This removes 22 of the 46 templates in that profile.
The remaining general blocker test removes 18 additional (1,2,2,4) templates.

## Four sources are possible, even with blocked insertion

Four sources mean there are no envy edges: the predecessor is envy-free. They do
NOT mean the omitted good can necessarily be inserted.

Here is an additive realization, with goods 0,...,9 and omitted good 9:

    14 14 22 3 17 8 19 3 3 14
    22 3 14 14 17 8 3 5 17 14
    22 3 17 8 14 14 19 3 3 14
    4 4 4 4 4 4 3 3 3 6

Take A=({0,1},{2,3},{4,5},{6,7,8}). The bundle values are

| Observer | A_0 | A_1 | A_2 | A_3 | g |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 28 | 25 | 25 | 25 | 14 |
| 1 | 25 | 28 | 25 | 25 | 14 |
| 2 | 25 | 25 | 28 | 25 | 14 |
| 3 | 8 | 8 | 8 | 9 | 6 |

Everyone strictly prefers their own bundle, so all four agents are sources.
Adding g to any pair is blocked by agent 3, since (2/3)(8+6)=28/3>9.
Adding g to the triple is blocked by each pair-agent, since
(3/4)(25+14)=117/4>28. The example satisfies (1)-(3), and exhaustive subset
checking finds no reachable safe champion. These properties survive the fixed
nondegenerate refinement from RESTORATION_LEMMAS.md. It is not certified to be
globally extremal, and is NOT an EFR or Mode C counterexample.

Indeed, swap omitted good 9 for good 1 in agent 0's pair. The new EFX predecessor
is ({0,9},{2,3},{4,5},{6,7,8}), omitting 1. Giving good 1 to agent 1 then gives
EFR. The nearest-predecessor oracle verifies minimum partition-edit distance two.
The full matrix and verified witness are in the saved example JSON.

## A sound reduced search, with an explicit scope boundary

`structural_efr_search.py` is a separate prototype. The existing unrestricted
Mode C oracle and campaign are not pruned or relabeled as having proven EFR.

For each remaining template the new search constrains a canonical starting A
to be EFX, fixes its envy graph, forbids all initial insertions, imposes (1)-(2),
and excludes every safe champion closing an envy path. It can sort row zero
within each old bundle by a simultaneous permutation of goods; it never sorts
valuation rows independently. No fixed-agent-priority-dependent transfer or
ownership-maximality cuts are imposed after symmetry reduction. Such cuts would
require tracking the priority ordering as part of the state.

A satisfying rational model goes to the unrestricted exact point oracle. Any
returned full EFR allocation excludes its entire EFR-feasible valuation region.
The cut uses the EFR inequalities alone, even when the witness was obtained by
Mode C; this is less restrictive than requiring that particular EFX predecessor.
If Mode C is absent at a point, the direct EFR oracle must also be exhausted before
calling it an EFR counterexample candidate. Timeouts remain OPEN.

If all necessary regions were certified empty after excluding successful EFR
witnesses, the extremal argument would prove EFR existence. It would not, without
an additional argument, prove universal Mode C or the old distance-five lemma.
An UNSAT result is exported for replay; the prototype labels it
UNSAT_REPLAY_PENDING rather than treating an unreviewed solver result as a finished
independent certificate.

## Runtime evidence and launch decision

The original local pilot selected nine templates, one for every occurring
(profile, source-count) combination. It gave each 15 seconds with three workers.
All nine remained OPEN; 538 rational candidates had valid EFR witnesses.
Total worker time was 135 seconds: 130.11 seconds (96.4%) in the solver and
2.73 seconds (2.0%) in the point oracle. These are worker totals, not serial wall
clock time. All nine selected cases remain in the final 156-template catalog.

A further 120-second run on the single four-source template reused its 64 prior
witnesses and reached 122 total witnesses, but remained OPEN. This is not evidence
that the region takes more than four days; it simply provides no completion-time
estimate.

The final linear-pair encoding was then run on the same nine templates, again
15 seconds per template with three workers. All nine remained OPEN, after 507
new rational candidates received valid EFR witnesses. No region closed in either
pilot, so this does not establish a proof-completion speedup. Witness counts
alone are not a measure of the fraction of a continuous region covered. No
wall-time cutoff is presented as a bound on proof completion time.

The 88.39% template reduction would correspond to an 8.62-fold reduction ONLY in
an artificial equal-cost-per-template model. We have not measured that speedup,
and it does not apply automatically to the old 220-root campaign. Solver difficulty
is highly unequal, and the current bottleneck is proving coverage, not finding
individual allocations.

Accordingly the user's condition for a complete GitHub search finishing within
three to four days has NOT been established. No multi-day GitHub search has been
launched. The code, exact reductions, examples, and local benchmark reports are
saved for review and further development.

Commands from the repository directory:

    python structural_reductions.py
    python -m unittest test_structural_reductions
    python structural_efr_search.py --pilot --seconds 15
    python structural_efr_search.py --pilot --seconds 15 --legacy-pairs

The optional --seed-directory imports only complete EFR allocation menus, never
previous proof statuses. --case selects an individual structural template. A
seconds budget limits an attempt, not the time needed to close a region.

The next focused proof task is to resolve the 140 remaining two-source templates
by source reachability and the restricted blocker sets, allowing either a terminal
EFR completion or a genuine fixed-potential improvement. Universal progress in
those templates remains unproved.

Dependency: BCFF restoration and its nondegeneracy handling are detailed in
RESTORATION_LEMMAS.md, based on Berger, Cohen, Feldman, Fiat, Theorem 5.1 in
https://arxiv.org/abs/2102.10654 (Theorem 4.1 in the AAAI version).
