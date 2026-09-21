# What EFX does and does not imply about insertion capacity

Assumptions throughout: nonnegative additive valuations; EFX0 (removing any good,
including a zero-valued one); EFR means comparison with the expected value after
uniformly removing one good from the other bundle. An empty target poses no envy.
Goods are indivisible and all old goods are allocated.

## 1. Exact criterion for a fixed predecessor

Let A be EFX, g unallocated, U_i=v_i(A_i), and s_k=|A_k|>0.
Insertion into k gives EFR if and only if, for every i != k,

    v_i(g) <= C_ik = ((s_k+1)/s_k) U_i - v_i(A_k).

Proof: averaging the EFX inequalities implies that A is EFR. All unchanged
nonrecipient comparisons stay valid, and the recipient's own utility increases.
Only comparisons against A_k union {g} remain. Their EFR inequalities are exactly
(s_k+1)U_i >= s_k(v_i(A_k)+v_i(g)). If A_k is empty, insertion is always safe.

Thus an exact obstruction is a directed blocking graph: i -> k iff i != k and
s_k(v_i(A_k)+v_i(g)) > (s_k+1)U_i. A recipient works precisely when its indegree
is zero. EFX alone does not ensure such a vertex.

## 2. Arbitrary fixed g: even the best predecessor may fail

All four agents value each of the nine old goods at 1 and g at 2. EFX forces
bundle sizes (3,2,2,2): largest size <= smallest size + 1, and sizes sum to nine.
For a size-two target, another size-two agent has capacity 3-2=1 < 2.
For a size-three target, a size-two agent has capacity 8/3-3=-1/3 < 2.
Therefore no EFX predecessor supports insertion of this fixed g.

This also rules out repairing this example merely by permuting the old bundles.
It does not rule out choosing a different deleted good or reallocating individual
goods before obtaining a final EFR allocation.

## 3. Even a universally least good can fail for a specified predecessor

Here is a strictly positive integer example. The old bundles are
A0={0,1,2}, A1={3,4}, A2={5,6}, A3={7,8}; g=9.

| Agent | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | g |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 2 | 2 | 2 | 6 | 6 | 1 | 1 | 1 | 1 | 1 |
| 1 | 1 | 1 | 1 | 3 | 3 | 6 | 6 | 1 | 1 | 1 |
| 2 | 1 | 1 | 1 | 1 | 1 | 3 | 3 | 6 | 6 | 1 |
| 3 | 3 | 3 | 3 | 1 | 1 | 1 | 1 | 3 | 3 | 1 |

Every own bundle has value 6. Agent 0 values A1 at 12 with either removal
leaving 6; similarly 1 values A2 and 2 values A3. Agent 3 values A0 at 9,
with every removal leaving 6. All remaining EFX comparisons have value <=6.
Thus A is EFX0, and g is weakly least-valued for every agent.

Yet agent 0 blocks target 1 with capacity (3/2)6-12=-3, agent 1 blocks target 2
with -3, agent 2 blocks target 3 with -3, and agent 3 blocks target 0 with
(4/3)6-9=-1. Every target fails even if g were worth zero!

The obstruction is a strict envy cycle 0 -> 1 -> 2 -> 3 -> 0.
Positive row normalization preserves every claim.

Run: `python capacity.py examples/least-good-fixed-predecessor.json`.
The program rotates that cycle and returns an exactly checked feasible insertion.

## 4. A sufficient condition using an unenvied bundle

Suppose A_k is nonempty and no other agent strictly envies its owner:

    U_i >= v_i(A_k) for every i != k.

If also v_i(g) <= v_i(A_k)/|A_k| for every i != k, then insertion is EFR.
Indeed,

    C_ik = (U_i-v_i(A_k)) + U_i/|A_k|
         >= v_i(A_k)/|A_k| >= v_i(g).

The average-value condition is weaker than requiring g to be no larger than
every individual good in the target. No requirement is needed for k's value of g.
This lemma holds for any number of agents and goods.

## 5. Repair theorem for a universally least-valued good

**Theorem.** If g is weakly least-valued by every agent among all goods, then
any complete EFX0 allocation of the old goods can be transformed, by permuting
whole bundles only, into an EFX0 allocation that permits insertion of g to get
EFR. This holds for any number of agents and old goods.

**Proof.** Form the strict envy graph i -> j when v_i(A_j)>v_i(A_i).
Whenever it contains a directed cycle, give each cycle agent the next agent's
bundle. Every affected agent strictly improves; every other agent keeps its
bundle. The unordered collection of bundles is unchanged.

EFX is preserved: for an observer, every bundle formerly belonging to another
agent was already bounded after any removal by the old own value. If the
observer's former own bundle becomes somebody else's, nonnegativity bounds its
value after removal by the old own value as well. The new own value is no smaller.

Cycles cannot continue forever: the agents' utility vector never decreases,
some coordinates strictly increase on each rotation, and only finitely many
permutations of the fixed bundles exist. With four agents there are at most
4!=24 ownership states, hence at most 23 cycle rotations.

The resulting acyclic envy graph has a vertex k of indegree zero. If its bundle
is empty, insertion is safe. Otherwise, because g is universally least,
v_i(g) <= v_i(A_k)/|A_k| for every i != k. Apply the preceding lemma. QED.

A run may stop earlier if any target already has capacity. `capacity.py` does so,
uses exact rational comparisons, and returns the rotations and margins. Without
the least-good assumption it is only a sufficient repair heuristic; failure is
not a counterexample to unrestricted Mode C.

## 6. What this settles, and the remaining theorem

The literal statement "every nine-good EFX allocation can accept an arbitrary
tenth good without changing the old allocation" is false. It remains false when
the tenth good is universally least-valued. Allowing whole-bundle rotations
repairs the latter statement, but not arbitrary fixed deletions.

The repair theorem proves Mode C for every instance having a universally
least-valued good, PROVIDED a complete EFX0 allocation of the remaining goods
exists. In particular, identical item rankings give such a good. The proof here
does not independently establish existence of that predecessor.

The unrestricted four-agent/ten-good statement remains:

    for every V, there exist g, an EFX0 predecessor A, and a recipient k
    such that v_i(g) <= C_ik(A) for all i != k.

Our sufficient condition reduces a potential proof to finding a deletion and an
EFX predecessor with an unenvied bundle meeting the average-value condition.
We have not proved that this condition can always be achieved. Different agents
need not share any least-valued good, and the capacity-blocking graph may still
have no zero-indegree vertex after strict envy cycles are eliminated. A failed
sufficient condition must not be counted as a refutation of Mode C.

These are self-contained proofs and regression examples, not a claim that the
lemmas are new in the literature or a proof of unrestricted additive EFR existence.
