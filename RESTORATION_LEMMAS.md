# Restoration with a fixed potential, and the remaining source obstruction

## Status and correction

The restoration step proposed in MODE_C_ADVERSARY_FINDINGS.md is available from
an existing theorem once we use a fixed lexicographic utility potential. We do
not need to prove restoration from scratch. The old sum-of-utilities potential
cannot simply be carried over: the imported theorem guarantees lexicographic
progress, not increasing total utility or Pareto improvement at every step.

What remains unproved is a universal way to initiate progress from a blocked
nine-good state with several envy-graph sources. This note proves restoration,
proves progress for a unique source of arbitrary bundle size, handles the
nondegeneracy reduction while preserving the supplied starting allocation, and
exhibits a verified obstruction to a more limited multiple-source repair rule.
No universal EFR existence proof or Mode C counterexample is claimed.

Throughout, EFX means EFX0 and valuations are nonnegative and additive. Envy edges
point from the envious agent to the envied agent. A source is unenvied.

## 1. Imported theorem and restoration corollary

Fix an ordering of the agents once and for all, and define

    Phi(X) = (v_0(X_0), v_1(X_1), v_2(X_2), v_3(X_3)),

ordered lexicographically. Work first with nondegenerate valuations: different
bundles have different values to each agent.

**BCFF progress theorem.** Every partial EFX allocation for four additive agents
with at least two unallocated goods admits another partial EFX allocation with
strictly larger Phi. This is Theorem 5.1 in the full version of Berger, Cohen,
Feldman, Fiat, and Theorem 4.1 in the AAAI version. Their dominance definition
uses a fixed arbitrary agent ordering. The paper assumes nondegeneracy in its
proof; Section 4 below supplies a starting-allocation-preserving reduction for
our setting rather than silently ignoring that assumption.

**Restoration corollary.** From any partial EFX state Y with at least two goods
unallocated, one can reach an EFX state Z allocating nine or ten goods with
Phi(Z) > Phi(Y).

**Proof.** Apply BCFF progress whenever two or more goods remain unallocated.
Every step strictly increases the same potential. There are at most 5^10 partial
allocations, counting the unallocated pool as a fifth destination. Consequently
the sequence cannot continue indefinitely. It must end with at most one good
unallocated. The endpoint is EFX and has greater potential. If it allocates all
ten goods, it is already EFR. QED.

The allocated-good count need not increase at each step. The potential ensures
termination. This is a proof using BCFF as a black box, not a new proof of their
case analysis or a polynomial-time guarantee.

## 2. Progress from a unique source, with no singleton restriction

**Lemma.** Let A be EFX on nine goods with omitted good g. Suppose the strict envy
graph is acyclic and has a unique source k. Either adding g to A_k yields EFR,
or there is a partial EFX allocation Y that Pareto improves A. Composing with
restoration gives either a complete EFX/EFR allocation or another EFX-nine
predecessor with strictly larger fixed lexicographic potential.

**Proof.** Put S=A_k and s=|S|. An empty S accepts insertion, so take s>0.
If agent i blocks EFR insertion, then

    v_i(A_i) < s/(s+1) * v_i(S+g).

Remove an i-least-valued good x from S+g. Its value is at most the average, so

    v_i((S+g)-x) >= s/(s+1) * v_i(S+g) > v_i(A_i).

Therefore some subset of S+g of cardinality at most s is envied. Choose T of
minimum cardinality among ALL subsets of S+g envied by ANY agent, and choose a
champion c with v_c(T)>v_c(A_c). By minimality, for every agent j and x in T,

    v_j(T-x) <= v_j(A_j).

Also g belongs to T: nobody envies S, and nonnegative valuations imply nobody
envies any subset of S. We have 1 <= |T| <= s.

Every vertex is reachable from the unique source in a finite DAG. Choose a
simple envy path k=a_0 -> ... -> a_t=c. Give a_r the old A_{a_{r+1}} for r<t,
and give c the bundle T. Leave other bundles unchanged. In the self-champion
case c=k, this simply replaces S by T.

All path agents strictly improve; everyone else is unchanged. Comparisons with
T after removal of any good are covered by minimality and weakly higher own
utilities. Comparisons with old bundles follow from original EFX; comparisons
against an observer's former own bundle also hold by nonnegativity and utility
improvement. Thus Y is EFX and Pareto improves A.

Exactly s+1-|T| goods are now unallocated. If this number is one, Y itself is a
better nine-good predecessor. Otherwise apply the restoration corollary. Every
Pareto improvement is an improvement in the fixed lexicographic potential, so
the restored endpoint still improves A in that potential. QED.

**More general version.** Uniqueness of the source is unnecessary whenever a
source has a reachable champion for a subset T satisfying the displayed safety
inequalities. The same proof works. The minimal-cardinality argument guarantees
a safe T, but does not guarantee reachability when several sources exist.

## 3. Structural consequence and the remaining proof obligation

In the nondegenerate/refined instance, choose an EFX allocation maximizing Phi
over all partial allocations. BCFF implies it leaves at most one good unallocated.
It has no strict envy cycle, since a cycle rotation would Pareto improve it.
If it is incomplete and its omitted good cannot be inserted to obtain EFR,
then the unique-source lemma implies that its envy graph has at least two sources.
More generally, it has no reachable safe champion from any source.

Thus the remaining configurations have two, three, or four sources. This is a
necessary condition on an extremal unresolved state, not a characterization of
counterexamples. A nonextremal state can have multiple sources and still admit
other improving repairs.

A sufficient missing theorem is:

> Every blocked EFX-nine state with multiple sources either admits a full EFR
> completion, or admits an EFX partial allocation with higher fixed potential.

Together with restoration and finiteness, this would give the broader
EFX-start-plus-moves-to-EFR construction. It is NOT proved here. A full EFX
endpoint produced during restoration suffices for EFR existence; without an
additional argument it is not necessarily a direct Mode C insertion witness.
The potential cannot be changed from one step to the next.

## 4. Preserving the supplied start when removing ties and zeros

An arbitrary generic perturbation can invalidate a given EFX starting allocation.
It is therefore insufficient to say only that generic valuations are dense.
Here is a perturbation that preserves our supplied start A.

If A has an empty bundle, insert g there and stop. Otherwise every A_i is nonempty.
Index goods 0,...,m-1 with m=10, set C=2^m, and define additive bonus values

    b_i(h) = C * 1[h in A_i] + 2^h.

For real valuations use w_i(h)=v_i(h)+epsilon*b_i(h), with epsilon>0 sufficiently
small to preserve every strict original subset comparison and every strict
original EFR comparison. There are finitely many such comparisons, so such an
epsilon exists. Fix it once for the entire execution.

- A remains EFX: on an originally tight constraint, b_i(A_i)>=C whereas the
  bonus on any subset of another old bundle is at most C-1.
- Every w_i is nondegenerate. On originally unequal subsets, sufficiently small
  epsilon preserves inequality. On equal-valued distinct subsets, their bonus
  sums differ: the own-good count contributes a multiple of C and distinct
  binary subset sums differ by a nonzero amount of absolute value below C.
- Every allocation EFX under w is EFX under v, since original strict violations
  were preserved. The same holds for EFR because its strict violations were also
  included among the comparisons whose signs are preserved.

The algorithm and BCFF restoration now run entirely under the fixed w, with
potential (w_0(X_0),...,w_3(X_3)). Every EFX intermediate state and EFR endpoint
is valid for the original instance. We do NOT claim that original total utility,
original lexicographic utility, or each original agent's utility increases at
every restoration step.

For rational inputs, independently scale each original row to primitive integers
v_i. Let B=max_i sum_h b_i(h), and use the explicit integer refinement

    K = 2(m+1)B+1,       w_i(h) = K*v_i(h)+b_i(h).

Every nonzero original subset difference has magnitude at least 1 and the bonus
difference has magnitude at most B. An EFR comparison
 t*v_i(U)-(t-1)*v_i(V), with t<=m, has bonus term of absolute value below 2(m+1)B.
Thus K preserves all relevant strict signs. `lift_preserving_start` implements
this exact construction and is tested on all 1024 subset values of each row.

## 5. A genuine obstruction to the limited source-path rule

The following positive additive matrix uses goods 0,...,9:

| Agent | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 4 | 4 | 8 | 1 | 8 | 1 | 1 | 5 | 1 | 4 |
| 1 | 3 | 1 | 9 | 1 | 3 | 8 | 5 | 1 | 1 | 7 |
| 2 | 1 | 1 | 1 | 1 | 5 | 1 | 2 | 1 | 1 | 5 |
| 3 | 19 | 1 | 17 | 1 | 19 | 1 | 7 | 7 | 7 | 14 |

Start with

    A=({0,1},{2,3},{4,5},{6,7,8}),     g=9.

Own utilities are (8,10,6,21). The envy edges are 0->1, 0->2, 1->2;
the sources are 0 and 3. All four insertions fail. Exhaustive checking of the
24 whole-bundle assignments shows that none permits insertion, and none that
is EFX has a larger lexicographic utility tuple than the given assignment.

All safe envied subsets of each source bundle plus g are exactly:

| Source | Safe envied subset | Champions | Reachable from source? |
| --- | --- | --- | --- |
| 0 | {0,9} | 3 | No |
| 3 | {7,9} | 0 | No |
| 3 | {6,9} | 1,2 | No |

Here safe means v_i(T-x)<=v_i(A_i) for every observer i and every x in T.
Consequently no source-path champion move of Section 2 applies. It is not valid
to combine the cross-source champion edges by using good 9 twice.

This obstruction survives the exact nondegenerate refinement of Section 4;
the test independently repeats all subset and ownership checks after lifting.
It is a counterexample to those LIMITED repair rules, not to Mode C or EFR.

## 6. One ordinary transfer escapes the obstruction

Move good 3 from agent 1 to agent 0:

    B=({0,1,3},{2},{4,5},{6,7,8}),     omitted good=9.

B is EFX and has utility tuple (9,9,6,21), lexicographically greater than A.
Agent 1 temporarily loses one unit, which is why Pareto-only repairs miss it.
Now insert good 9 into agent 1's singleton. The full EFR allocation is

    ({0,1,3},{2,9},{4,5},{6,7,8}),

with own utilities (9,16,6,21). Both the EFX predecessor and EFR endpoint remain
valid under the fixed refinement used above. This escape needs one membership
change and does not change the omitted good.

For systematic transfer search define R_i(S)=v_i(S)-min_{h in S}v_i(h), with
R_i(empty)=0. Moving h from A_j to A_i preserves EFX exactly when:

1. For every observer l other than i,j,
       v_l(A_l) >= R_l(A_i+h).
2. The donor satisfies all new comparisons,
       v_j(A_j)-v_j(h) >= max_{k != j} R_j(B_k).

All other comparisons follow from original EFX, increased recipient utility,
and the fact that shrinking a target bundle cannot increase R. If i precedes j
in the fixed priority order and v_i(h)>0, this is a strict lexicographic progress
move. These inequalities are a checkable criterion, not a proof that such a
transfer must always exist.

## 7. The obstruction also occurs with no common least good

A second exact example has valuation rows

    30 5 6 6 1 1 1 1 1 24
    11 9 1 1 1 1 2 2 2 8
    9 19 6 6 7 1 1 1 1 6
    4 1 2 7 1 3 3 1 3 8

Start at ({0},{1},{2,3},{4,5,6,7,8}) and omit 9. There is no common least-valued
good. Sources are agents 2 and 3, and the envy edges are 2->1->0. As in Section 5,
all insertions and all whole-bundle reassignment attempts fail, the starting
assignment is lexicographically maximal among EFX ownerships, and no reachable
safe champion exists. This is verified by enumerating subsets and all 24 owners.

Move good 4 from agent 3 to agent 2. The resulting EFX-nine allocation has own
utilities (30,9,19,10), compared with the original (30,9,12,11). Insert good 9 into
agent 1's singleton to obtain full EFR utilities (30,17,19,10). The final agent 3
need not recover the lost value: the construction guarantees fairness and a
fixed potential, not Pareto domination of the original allocation. This example
and escape also survive our exact nondegenerate refinement.

The bounded integer search found three such no-common-minimum local obstructions,
with starting profiles (1,1,2,5), (1,2,2,4), and (2,2,2,3). Each has an EFX-to-EFR
escape at exactly one changed membership, allowing whole-bundle reassignment.
These are finite examples, not a profile classification. In the last example,
no single transfer from a later-priority donor to an earlier-priority recipient
preserves EFX, but a transfer in the opposite direction allows immediate EFR
completion. A terminal EFR completion need not improve the intermediate potential;
potential progress is required only for nonterminal iterations.

## Reproducibility and next task

- `restoration_moves.py`: exact refinement, reachable safe champion moves, and
  lexicographically improving one-good transfers. It does NOT implement BCFF's
  full restoration case analysis.
- `search_restoration_obstruction.py`: bounded positive integer SMT search for
  an obstruction to the limited source-path and ownership rules. No EFR
  nonexistence claim is made by this script.
- `test_restoration_moves.py`: four tests verify the multiple-source obstruction,
  its escape, the no-common-minimum variants, the nondegenerate refinement, and the release of six goods from
  our earlier large-source example. All four passed.
- `experiment-results/restoration/verified-two-source-obstruction.json`: the
  matrix, exhaustive source-subset analysis, explicit lift, and valid completion.

The focused next task is to combine potential-improving ordinary transfers with
champion exchanges for the remaining two/three/four-source configurations. The
example motivates allowing temporary losses for later-priority agents. No arbitrary-start five-change bound is required for this route.

References:

Berger, Cohen, Feldman, Fiat, *(Almost Full) EFX Exists for Four Agents (and
Beyond)*, full version https://arxiv.org/abs/2102.10654, Theorem 5.1 and the
nondegeneracy convention in Section 2. AAAI version:
https://doi.org/10.1609/aaai.v36i5.20410, Theorem 4.1.

## Follow-up: structural search reductions

[STRUCTURAL_REDUCTIONS.md](STRUCTURAL_REDUCTIONS.md) strengthens the singleton-source
argument, proves safe-pair and restricted-blocker lemmas, and reduces the extremal
EFR obstruction catalog from 1344 to 156 structural templates. It includes a
four-source blocked example and local timing evidence. The complete three-to-four
day search condition remains unsupported; no multi-day run was launched.
