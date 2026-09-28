# EFX-nine to EFR-ten: research status and proof roadmap

Latest focused results (2026-09-28): [three-source targets and return](research/THREE_SOURCE_TARGETS_AND_RETURN.md)
proves D21 (singleton pair champion repairs mutual triple danger outside the
D17 guard), D22 (a sole forbidden-pair observer reachable from the quad source
admits a champion transfer), and D23 (reverse dangerous-item transfer with
budgeted compensation, including a proof that singleton blockers are repairable).
For the two-singleton triple-source branch, the new residual condition is that
all 16 donor subsets fail the compensation value/budget criterion. No complete
graph template is closed; all three results give Pareto progress under their
explicit hypotheses and preserve every fixed priority.

Latest two-singleton results (2026-09-28): [after joint-split failure](research/AFTER_JOINT_SPLIT_FAILURE.md)
proves D19: a pair source reaching both singleton owners has an EFR insertion
or Pareto escape if the other source's pool value is at most half its utility.
This excludes the dominant-donor terminal branch in six open (1,1,2,5) graphs.
D20 reduces eleven reachable (1,1,3,4) graphs under the dominant-donor cuts to
at most one dangerous removal item and an explicit source-utility obstruction.
A different singleton assignment retains the dominant item and repairs joint-
split failure examples, which also admit elementary source replacements.
These are conditional valuation-region reductions, not whole-graph closures.

Latest structural split (2026-09-28): [two-source versus three-source strategies](research/TWO_VS_THREE_SOURCES.md)
adds D16 (joint surplus and compensation), D17 (the guarded triple exchange
kernel does not need the pair owner to envy the singleton), and D18 (four-good
source replacements reduce to forbidden-pair intersections). The previous
unsafe-top-up example now has a complete EFX Pareto escape. Empty intersections
have disjoint-pair or triangle certificates. These are local reductions; no
whole graph is newly closed. Of the 94 two-source rows, only 31 have the two
singleton targets assumed by the current surplus implementation.

Preceding local results (2026-09-28): [singleton blockers and donor top-ups](research/SINGLETON_BLOCKER_TOP_UP.md)
adds D14 (exact augmentation conditions, at most six minimal top-ups per blocker)
and D15 (the blocker's surplus bounds top-up deletion values). Explicit examples
repair cheap singleton blockers in both priority branches and an early champion
blocker. Another exact example has 20 units available for a deficit of 9 but
no safe top-up; it nevertheless has a verified Mode C witness. An additional
blocker's gain may change which losses are allowed under the same fixed priority.
The atlas remains unchanged. The preceding [D12–D13 analysis](research/DOMINANT_ITEM_OBSTRUCTION.md)
provides the minimal covers and blocker subsets used here.

Previous whole-case update (2026-09-27): [T11 and failure-case analysis](research/FULL_STAR_AND_FAILURE_CASES.md)
closes the entire `1233_248` graph, including the sole-champion/later-priority
branch, by Pareto improvements. The current count is 102 open graphs: 94 with
two sources and 8 with three. Priority-decorated representatives total 2,280.
The earlier source-compensation and dangerous-item notes are retained as the
proof history; their 103-case counts are historical.

**Consolidated status: 28 September 2026.** Four agents, ten indivisible goods,
nonnegative additive valuations, and EFX0 throughout. This is the current index
of the project; older notes contain the detailed proofs and historical runs.
No claim of novelty in the literature is made for the elementary lemmas.

## Abstract

We study whether an EFX allocation of nine goods can be used to obtain an EFR
allocation of ten goods. Exact insertion capacities, safe replacement rules,
restoration with a fixed lexicographic potential, and coordinated-source moves
give several positive results. Counterexamples show that a prescribed omitted
good, a prescribed size profile, size-preserving exchanges, and two-agent
monotone repair are each insufficient in general. None of these examples
refutes unrestricted EFR existence or Mode C. The current necessary extremal
case decomposition has 1,344 acyclic nonempty templates: 1,190 are excluded by
human proofs, 52 more by computer-checked propositions, and 102 remain open.
The open templates consist of 94 two-source and 8 three-source cases.

## 1. Definitions and the three different questions

Let M={0,...,9}, N={0,1,2,3}, and v_i(S)=sum_{h in S} v_i(h). A partial
allocation assigns each good to at most one agent. EFX means

    v_i(A_i) >= v_i(A_j minus {h})  for every i!=j and h in A_j.

EFR compares an agent's own bundle with the expectation after uniformly
removing one item from the other bundle. Under additivity this is exactly

    |X_j| v_i(X_i) >= (|X_j|-1) v_i(X_j).

An empty target contributes zero. EFX implies EFR by averaging.

| Question | Quantifiers and allowed changes | Current answer |
| --- | --- | --- |
| **G1: unrestricted EFR existence** | Every additive 4x10 instance has some complete EFR allocation. | **OPEN in this project; no counterexample found.** |
| **G2: Mode C** | For every instance, some omitted good g, some complete EFX predecessor on M minus {g}, and some recipient give EFR by insertion. | **OPEN; no counterexample found.** |
| **G3: distance-five escape** | From every supplied EFX-nine start, some extendable EFX predecessor is at partition-edit distance at most five; g may change. | **OPEN; five is necessary on a proved family.** |
| **G4: general fixed-potential progress** | Every blocked EFX-nine state admits EFR completion or an EFX improvement in the same fixed potential, allowing multiple unallocated goods. | **OPEN; would close the restoration route.** |
| **G5: three-agent local progress** | The preceding progress can always be achieved while changing at most three agents' bundles. | **OPEN candidate, not needed if a broader progress lemma is found.** |

G3 implies G2 when a predecessor exists, and G2 implies G1. The converses are
not established. A complete EFX endpoint produced during restoration is EFR,
but does not automatically supply a Mode C certificate. A failed local rule
does not refute G1 or G2.

Partition-edit distance matches old and new physical bundle slots optimally;
whole-bundle ownership changes are free. It counts the omitted-good slot too:

    d((A,g),(B,h))=10-1[g=h]-max_p sum_i |A_i intersect B_{p(i)}|.

Thus an omitted-good exchange costs two memberships. This metric differs from
the number of agents whose bundles change.

## 2. The extremal proof framework

Fix agent priority once and maximize the tuple of own utilities
Phi(X)=(v_0(X_0),...,v_3(X_3)) lexicographically over partial EFX allocations.
There are finitely many partial allocations. The imported BCFF progress theorem
rules out an extremal generic allocation with at least two unallocated goods.
A complete endpoint is already EFR; otherwise it allocates nine goods.

A strict envy cycle or any EFX Pareto improvement contradicts extremality.
The remaining lemmas exclude further terminal configurations. If all remaining
configurations are excluded, G1 follows. This is why the case atlas labels
**terminal obstructions**, not all allocations or all valuation profiles.

The boundary arguments are already available: a positive generic perturbation
preserves the finitely many strict failures of a hypothetical no-EFR instance;
and the stronger supplied-start-preserving refinement in
[RESTORATION_LEMMAS.md](RESTORATION_LEMMAS.md#4-preserving-the-supplied-start-when-removing-ties-and-zeros)
preserves an arbitrary nonempty EFX start and maps fair outputs back. Do not
replace this with an arbitrary perturbation of a supplied EFX allocation.

<a id="theorem-register"></a>
## 3. Theorem and proposition register

These labels are used in every cell of [CASE_ATLAS.md](CASE_ATLAS.md). A T label
has a human-readable argument; T4 explicitly imports a published theorem.
CP labels are computer-checked statements, not mislabeled hand proofs.

<a id="t1"></a>
### T1. Exact capacity and empty-bundle insertion

For an EFX predecessor A, omitted good g, u_i=v_i(A_i), and s=|A_k|>0,
insertion into k is EFR iff

    (s+1)u_i >= s(v_i(A_k)+v_i(g))  for every i!=k.

All other comparisons survive automatically. An empty bundle always accepts
g. This closes the twelve size profiles containing zero.
Proof: [EXTENSION_THEORY, Section 1](EXTENSION_THEORY.md#1-exact-criterion-for-a-fixed-predecessor).

<a id="t2"></a>
### T2. Envy-cycle elimination

Rotating a strict envy cycle gives an EFX Pareto improvement. The unordered
bundle collection is preserved, own utilities do not decrease, and old-own-
bundle comparisons follow from nonnegativity. Hence terminal envy graphs are
acyclic. Proof: [EXTENSION_THEORY, Section 5](EXTENSION_THEORY.md#5-repair-theorem-for-a-universally-least-valued-good).

<a id="t3"></a>
### T3. Common-least-good repair and the source-average criterion

A source k admits insertion if every other agent values g no more than the
average value of A_k. In particular, if g is weakly least-valued by all agents,
cycle elimination followed by insertion into a source succeeds. This proves
Mode C for the common-least-good subclass given EFX-nine existence. It does
not apply when the agents have different least goods.
Proof: [EXTENSION_THEORY, Sections 4-5](EXTENSION_THEORY.md#4-a-sufficient-condition-using-an-unenvied-bundle).

<a id="t4"></a>
### T4. Restoration with a fixed potential

For four nondegenerate additive agents, a partial EFX allocation with at least
two unallocated goods has a lexicographically improving partial EFX successor.
Iterating the BCFF progress theorem terminates at an EFX allocation with at
most one good unallocated. The potential is fixed throughout. It is not a
sum-of-utilities or stepwise Pareto guarantee. The boundary refinement above
handles zeros and ties for the original problem.
Proof and attribution: [RESTORATION_LEMMAS, Sections 1 and 4](RESTORATION_LEMMAS.md#1-imported-theorem-and-restoration-corollary).

<a id="t5"></a>
### T5. Unique-source progress

If an acyclic EFX-nine state has one source, either insertion succeeds there
or a minimum-cardinality envied subset of the source bundle plus g is safe.
Its champion is reachable from the unique source. Rotating the path and
assigning that subset Pareto improves EFX; T4 handles released goods. This
holds for any source bundle size.
Proof: [RESTORATION_LEMMAS, Section 2](RESTORATION_LEMMAS.md#2-progress-from-a-unique-source-with-no-singleton-restriction).

<a id="t6"></a>
### T6. Pool envy and singleton sources

At an extremal state v_i(g)<=u_i for every i: otherwise replace A_i by {g}.
If a source owns {h}, a blocker would require 2u_i<v_i(h)+v_i(g), while
v_i(h)<=u_i, contradicting the pool bound. Thus a blocked terminal state has
no singleton source. Combined with T5, this excludes profile (1,1,1,6).
Proof: [STRUCTURAL_REDUCTIONS, Lemmas 1-2](STRUCTURAL_REDUCTIONS.md#lemma-1-the-omitted-good-cannot-be-envied-at-an-extremal-state).

<a id="t7"></a>
### T7. Safe pairs and restricted blockers

If h is in an old bundle of size at least two and the pool bound holds, {g,h}
is safe against every one-good removal. A reachable champion gives an EFX
improvement. Hence, at extremality, v_i(g)+v_i(h)<=u_i whenever the owner of h
reaches i. In particular a pair owner values g at most its least own item.
A two-good source therefore needs a blocker who is both unreachable from it
and owns a bundle whose size differs from two. Templates without such a
blocker are excluded.
Proof: [STRUCTURAL_REDUCTIONS, Lemmas 3-4](STRUCTURAL_REDUCTIONS.md#lemma-3-a-two-good-bundle-containing-g-is-automatically-safe).

<a id="t8"></a>
### T8. Two-agent compensation

Let A_k={h,x}, |A_i|>=2, and v_i(g)+v_i(h)>u_i. If some y in A_i satisfies
v_k(y)>=v_k(h), replacing A_i by {g,h} and A_k by {x,y} is an EFX Pareto
improvement. Both new bundles are safe pairs. Neither agent needs to be a
source. This yields exact necessary inequalities for a terminal obstruction.
Proof: [TWO_SOURCE_PROGRESS, Section 1](TWO_SOURCE_PROGRESS.md#1-safe-pairs-and-compensation).

<a id="t9"></a>
### T9. Four-source progress

Every EFX-nine state with four sources has an EFR insertion or an EFX Pareto
improvement. After elementary cases, the profile is (2,2,2,3). The triple owner
blocks each pair. Either T8 compensates a pair owner, or the triple owner can
safely replace an old item by g and improve. Four sources are possible at an
arbitrary start, but cannot be terminal.
Proof: [TWO_SOURCE_PROGRESS, Section 2](TWO_SOURCE_PROGRESS.md#2-four-sources-cannot-be-a-terminal-obstruction).

<a id="t10"></a>
### T10. Three-agent compensated path: sufficient conditions

For distinct s,i,t, choose h in A_t, |A_t|>=2, with v_i(g+h)>u_i and
v_s(A_i)>=u_s. Set B_s=A_i, B_i={g,h}, B_t=A_s. The pool bound makes the new
pair safe. If i precedes t and the donor satisfies all its new EFX comparisons,
B is EFX and strictly increases the same lexicographic potential. The donor
may lose utility. This is a proved sufficient lemma, **not** a guarantee that
the needed agents and compensation always exist.
Proof: [TWO_SOURCE_PROGRESS, Section 4](TWO_SOURCE_PROGRESS.md#4-a-three-agent-compensated-path-lemma).

<a id="t11"></a>
### T11. Full all-envious-source (1,2,3,3) star

If the three nonsingleton owners are sources and all envy the singleton, then
there is an EFR insertion or a partial EFX Pareto improvement. The sole-champion
branch reduces to mutual danger or split danger; both have constructive repairs
independent of priority. Thus `1233_248` is excluded as a terminal obstruction.
Proof: [full-star theorem](research/FULL_STAR_AND_FAILURE_CASES.md#t11).

<a id="cp1"></a>
### CP1. Compensation exclusions

The exact necessary extremal constraints plus the absence of T8 are infeasible
in 50 of the historical 156 templates. One of these also has the T9 human
proof, so the atlas uses CP1 for the other 49. Z3 and cvc5 returned UNSAT;
cvc5 internal proof checking was enabled. The retained input classification is
[all-compensation.json](experiment-results/two-source/all-compensation.json),
with [replay records](experiment-results/two-source/cvc5-replay.json).

<a id="cp2"></a>
### CP2. The last three balanced extremal templates

The three templates 2223_003, 2223_011, and 2223_013 are covered by finite menus
of EFR completions or EFX Pareto improvements. Their menu sizes are 41,30,30.
The complement is UNSAT in both solvers. Together with earlier reductions,
this closes the entire (2,2,2,3) terminal profile in the encoded proof route.
The three retained JSON menus and SMT2 inputs are in
[experiment-results/two-source](experiment-results/two-source/).

CP1/CP2 cover continuous valuation regions; they are not conclusions from finite
sampling. They still trust the extremal reduction, its Python encoding, and
solver implementations; there is no end-to-end proof-assistant verification.
The canonical replay has 53 distinct inputs. An earlier 54-input run checked
the four-source case twice; the duplicate was removed in the cleanup.

## 4. Counterexample register: exactly what fails

| Label | Refuted statement | Witness and explanation | What remains possible |
| --- | --- | --- | --- |
| N1 | Every prescribed omitted good admits some extendable EFX predecessor. | Identical values: nine units and a prescribed extra good worth 2. All nine-good EFX predecessors fail insertion. [Proof](EXTENSION_THEORY.md#2-arbitrary-fixed-g-even-the-best-predecessor-may-fail). | Another omitted good; Mode C; EFR. |
| N2 | Every specified EFX predecessor directly accepts even a common least good. | A strict envy-cycle example blocks every target, even for value-zero addition. [Proof](EXTENSION_THEORY.md#3-even-a-universally-least-good-can-fail-for-a-specified-predecessor). | T2/T3 repair the ownership assignment. |
| N3 | Only balanced (2,2,2,3) predecessors need examination for Mode C. | Identical values (100,1,...,1): a balanced EFX predecessor must omit the large good, which cannot be inserted. [Matrix](examples/balanced-predecessor-obstruction.json). | Unbalanced predecessors can work. Closing balanced *terminal* states does not contradict this example. |
| N4 | Ownership changes and EFX-preserving omitted-good exchanges always escape. | Four H goods and six units, 6<H<36, starting at (1,1,1,6). The move invariant traps the component. Also verified disconnected traps within (2,2,2,3). [Proof and cases](EXCHANGE_FINDINGS.md). | Coordinated changes that alter sizes or leave the exchange component. |
| N5 | Fewer than five partition-membership changes always suffice. | The same H family has minimum escape distance exactly five. [Proof](REBUNDLING_LEMMAS.md#lemma-4-five-simultaneous-membership-changes-can-be-necessary). | A universal upper bound of five is still open. |
| N6 | Two-agent changes always give fixed-potential EFX progress or complete EFR. | A positive nondegenerate two-source example exhausts all 8,532 local repartitions without either outcome. Three agents escape. [Verified witness](experiment-results/two-source/verified-obstruction.json), [proof scope](TWO_SOURCE_PROGRESS.md#3-two-agent-monotone-repair-is-not-universal). | Broader moves, other priorities, or a temporary decrease of the chosen potential. |

The weaker source-path and whole-bundle-only obstructions in
[RESTORATION_LEMMAS.md](RESTORATION_LEMMAS.md) are retained as regression examples;
some escape by an ordinary transfer. N6 is the stronger current locality limit.
The fixed priority in N6 matters: simultaneous failure for every possible
priority was not proved. No entry in this table is an overall EFR counterexample.

The attached monotone-valuation counterexample has a different domain. Even its
strict pair preferences violate additive cancellation: its agent 0 requires
v({1,2})>v({1,4}) and v({4,5})>v({2,5}), which would imply both v(2)>v(4) and
v(4)>v(2). Its exponential amplification therefore cannot be imported into an
additive instance. See [TWO_SOURCE_PROGRESS, Section 6](TWO_SOURCE_PROGRESS.md#6-what-the-attached-monotone-counterexample-teaches-us).

## 5. Current case ledger

The full [case atlas](CASE_ATLAS.md) contains all 18 starting size profiles,
the size/source-count matrix, and 1,344 individual canonical acyclic graph rows.
Each detailed row is labeled by its closing theorem/proposition or **OPEN**.

| Nonempty profile | Acyclic templates | Human proof | Additional computer check | OPEN |
| --- | ---: | ---: | ---: | ---: |
| (1,1,1,6) | 104 | 104 | 0 | 0 |
| (1,1,2,5) | 284 | 266 | 5 | 13 |
| (1,1,3,4) | 284 | 266 | 0 | 18 |
| (1,2,2,4) | 284 | 245 | 13 | 26 |
| (1,2,3,3) | 284 | 228 | 11 | 45 |
| (2,2,2,3) | 104 | 81 | 23 | 0 |
| **Total** | **1344** | **1190** | **52** | **102** |

The twelve empty-bundle profiles are closed separately by T1. Strict envy cycles
are removed by T2 before this acyclic count. Counts quotient only by simultaneous
agent relabelings preserving bundle sizes. They do not independently sort rows.
The 102 open cases are 94 two-source and 8 three-source cases, each representing
an infinite valuation region. They do not correspond one-to-one to the older
220 valuation-ranking roots of the Mode C campaign.

## 6. Experiments and implementation: what the evidence supports

| Work | Verified outcome | Limitation |
| --- | --- | --- |
| Exact point oracle | 11,051 unlabeled partitions per deletion; matching over all ownerships; exact integer/rational arithmetic and overflow fallback. | Fast point checks do not measure continuous-domain proof time. |
| GitHub exchange run 35576951293 | 136 starts on 80 generated profiles: 108 direct insertions, 7 ownership repairs, 12 exchange repairs, 9 certified restricted traps. Every trap had an unrestricted extension. | Finite generated test set. |
| GitHub rebundling run 35597667294 | All 113 starts escaped; exact minimum distances included six instances requiring five changes. | Does not prove the distance-five upper bound. |
| All-deletion adversarial runs | 592 successful exact candidate/witness checks; all three symbolic domains ended UNKNOWN. | No domain coverage or counterexample. |
| Seeded mutation search | 404 candidate evaluations; the smallest observed number of successful omitted goods was six. | Six is not a universal lower bound. |
| Earlier full-region pilot | Zero of 220 roots closed in the recorded 90-second attempt. | Budget expiration is not a negative theorem. |
| Structural pilots | Both nine-case pilots closed zero regions; the longer four-source attempt also remained open. | Superseded by theoretical compensation reductions for that case; no general runtime estimate. |
| Coordinated-source certificates | 53 distinct historical-156 regions excluded, one also by T9; independent cvc5 replay. | 103 remained after these checks; T11 reduces the live ledger to 102. Semantic encoding not formally verified. |

Canonical evidence is indexed in [experiment-results/README.md](experiment-results/README.md).
The earlier 88.4% template reduction and the current smaller case count are
combinatorial reductions, not measured wall-time speedups. No complete search
within three to four days has been justified, and no new long workflow is
launched by this consolidation.

<a id="roadmap"></a>
## 7. Theoretical roadmap before another exhaustive campaign

### Step A: choose the claim and the invariant explicitly

For the current route, target G1 using one fixed lexicographic potential. State
the desired progress disjunction precisely: a complete EFR endpoint, or a
partial EFX allocation with a larger fixed potential. T4 then restores nine or
ten allocated goods and finiteness gives termination. If G2 is the target,
also prove that the endpoint has an EFX-nine deletion certificate; T4 alone
does not give that implication. Keep G3 as a separate stronger conjecture.

### Step B: settle the eight remaining three-source templates

These are explicitly listed at the top of [OPEN_CASES.md](research/OPEN_CASES.md).
Four have profile (1,2,2,4), and four have (1,2,3,3). Every envy edge in these
eight graphs points into agent 0's singleton. This common topology is a concrete
target for a unified lemma: use the singleton as the end of a path, then
compensate a second source without reusing g. Prove a capacity or compensation
inequality that forces completion or strict progress. T11 has now settled the all-envious-source (1,2,3,3) row; the other eight
stars remain open.

### Step C: strengthen T10 for the 94 two-source templates

The central missing statement is not another safe-pair check. It is a guarantee
that some donor can accept the compensating bundle while preserving EFX, or
that failure of all such compensation conditions forces a direct EFR outcome.
Use N6 as a required stress test: a universal argument restricted to two
changing agents and this potential is already false. Allow at least three
agents, released goods, and a loss for a later-priority donor when its remaining
EFX inequalities permit it. Do not assume three agents always suffice.

For a proposed compensated path, explicitly prove the donor inequality

    v_t(A_s) >= max_{j!=t, h in B_j} v_t(B_j minus {h}),

and strict increase of the same potential. A promising alternative is to show
that failure yields a finite additive-cancellation contradiction or a different
champion path. Any matching/Hall formulation must also enforce disjointness:
two champion edges cannot both consume the single omitted good.

### Step D: repair the symmetry before using lexicographic search cuts

The current 102-case reduction uses priority-independent Pareto improvements.
Sorting bundle sizes and canonicalizing the graph may permute agent priority.
T10 is priority-dependent. Either prove its use uniformly over priority orders,
or carry the priority ordering as part of the case and quotient it together
with the graph. A fixed-priority inequality cannot silently be added to the
current canonical cells. The current exact decorated count is 2,280: 2,136 for two-source graphs and
144 for three-source graphs. The generator `python -m efr.priority` carries
priority through the graph automorphisms.

### Step E: make the remaining computer argument small and auditable

Try to replace CP1's graph-specific solver exclusions and CP2's 101 total menu
entries with short structural proofs or smaller witness menus. For any new
move family, prove necessity of every exclusion clause and retain explicit
success witnesses. Keep zeros/ties, strict failure inequalities, row scaling,
and ownership conventions in the proof statement. The boundary work is already
available; it needs to be applied consistently, not reproved from scratch.

Only then benchmark closure of actual remaining regions using the new encoding.
Measure completed continuous-region certificates, solver time, verification
time, and memory. A useful long-run plan needs demonstrated closure or a justified
finite bound on the outstanding certificate work. Candidate throughput and
wall-time caps alone cannot predict a three-to-four-day completion.

## 8. References and navigation

- Berger, Cohen, Feldman, Fiat: [(Almost Full) EFX Exists for Four Agents (and Beyond)](https://arxiv.org/abs/2102.10654). Full-version Theorem 5.1 / AAAI Theorem 4.1 supplies the progress dependency. We do not claim this theorem as our contribution.
- Alkassar, Fouz, Mehlhorn: [Complete EFX Allocations Exist for Four Additive Agents and Up to Nine Goods](https://arxiv.org/abs/2608.08590). External EFX-nine existence result; its full certificate corpus was not rerun here.
- [CASE_ATLAS.md](CASE_ATLAS.md): theorem/open matrix and every individual structural case.
- [research/OPEN_CASES.md](research/OPEN_CASES.md): the 102 unresolved case IDs and exact envy graphs.
- [TWO_SOURCE_PROGRESS.md](TWO_SOURCE_PROGRESS.md): newest full proofs and locality obstruction.
- [RUNNING.md](RUNNING.md): operational instructions; these are not completion-time promises.
- [experiment-results/README.md](experiment-results/README.md): retained evidence and cleanup policy.
