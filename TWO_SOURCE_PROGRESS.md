# Coordinated repairs: a four-source theorem and a two-agent obstruction

Current consolidated index: [RESEARCH_STATUS.md](RESEARCH_STATUS.md).
The theorem/open matrix is [CASE_ATLAS.md](CASE_ATLAS.md).

## What has and has not been established

There are three different results here:

1. A human-readable proof: a nine-good EFX allocation with four envy-graph
   sources always admits either an EFR insertion or a Pareto-improving partial
   EFX allocation. Thus four sources cannot occur at an extremal obstruction.
2. An exact, independently enumerated counterexample to **two-agent local
   lexicographic progress**, even with positive nondegenerate additive values.
   The other two agents' bundles are held fixed. A three-agent move escapes it.
3. Computer-checked exclusions reduce the previous 156 necessary extremal
   templates to 103. All 24 remaining (2,2,2,3) templates are excluded. These
   exclusions are reproduced with Z3 and cvc5, with cvc5 proof checking enabled.

No counterexample to unrestricted EFR existence or Mode C was found. No universal
three-agent progress lemma has been proved. The two-agent obstruction concerns
a specified fixed priority, not every possible choice of priority.

Throughout, EFX is EFX0, valuations are nonnegative additive, envy edges point
from an envious agent to the envied agent, and a source is unenvied. Let A be an
EFX allocation of nine of the ten goods, g the omitted good, and u_i=v_i(A_i).
Restoration after releasing several goods uses the BCFF theorem explained in
RESTORATION_LEMMAS.md; it is not implemented by the local-move routines.

## 1. Safe pairs and compensation

Assume v_j(g)<=u_j for every j. If h belongs to an old bundle with at least two
goods, then v_j(h)<=u_j for every j. For its owner this is nonnegativity; for
other agents apply EFX after removing another item from h's old bundle.
Consequently every deletion from {g,h} is worth at most u_j to every observer.
The same is true of a pair of old goods from bundles of size at least two.

**Compensation lemma.** Suppose A_k={h,x}, |A_i|>=2, i!=k, and some y in A_i
satisfies

    v_i(g)+v_i(h)>u_i,       v_k(y)>=v_k(h).

Give {g,h} to i and {x,y} to k; leave the other agents unchanged and release
unused goods. This is an EFX Pareto improvement.

**Proof.** Agent i improves strictly and k does not lose. Both new bundles are
safe pairs by the preceding observation. Unchanged bundles remain EFX targets
because nobody's own utility decreased. The bundles are disjoint. QED.

Neither agent must be a source, and reachability is unnecessary. The necessary
condition for an extremal obstruction is therefore the disjunction

    v_i(g)+v_i(h)<=u_i   OR   v_k(y)<v_k(h).

This is what compensation_cuts encodes. Failure of this particular move does
not imply failure of more general coordinated repairs.

## 2. Four sources cannot be a terminal obstruction

**Theorem.** If A has four sources, either some insertion of g is EFR, or there
is a partial EFX allocation that Pareto improves A.

**Proof.** Four sources means A is envy-free. An empty bundle admits insertion.
If some agent values g above its own bundle, replacing that bundle by {g} is an
EFX improvement. We may therefore assume v_i(g)<=u_i for all i.

If there is a singleton bundle, insertion into it is EFR: for every observer,
the old singleton and g are each worth at most that observer's own bundle.
Thus, if no insertion works, the bundle sizes must be (2,2,2,3).

Let t own the triple T and let z=v_t(g). If any agent can improve by replacing
its bundle with a pair {g,h} drawn from its own bundle, do so. Otherwise,

    v_i(g)<=min_{h in A_i} v_i(h)             for each pair owner i,
    z+v_t(y)<=u_t                            for every y in T.       (1)

A pair owner cannot block insertion into another pair: the target is unenvied
and its omitted-good value is at most half its own utility. Therefore t blocks
insertion into every pair A_i. Since v_t(A_i)<=u_t, this implies

    2(v_t(A_i)+z)>3u_t,     hence z>u_t/2.                        (2)

For each pair owner i there is h_i in A_i with

    z+v_t(h_i)>u_t.                                              (3)

Indeed, blocking implies some two-good subset of A_i+g is envied by t, by
average deletion. It cannot be A_i itself, which is unenvied, so it contains g.

If v_i(y)>=v_i(h_i) for some i and y in T, the compensation lemma applies:
t receives {g,h_i}, and i receives its retained item together with y.

Otherwise, for every pair owner i and y in T,

    v_i(y)<v_i(h_i)<=u_i-v_i(g).                                 (4)

The last inequality follows from the pair-owner bound in (1). Replace any
item y_0 of T by g. The triple owner strictly improves, since (1)-(2) give
v_t(y_0)<=u_t-z<z. To verify EFX, consider any pair left after deleting an item
from the new triple. An old pair from T is safe by original EFX. A pair {g,y}
is safe to every pair owner by (4), and to t by (1). Other targets are unchanged.
Thus this replacement is a Pareto-improving EFX allocation. QED.

This theorem holds even with zeros and ties. The compensation move can leave
two goods unallocated; restoring nine or ten allocated goods uses the earlier
fixed-potential restoration result and its nondegeneracy treatment. This rules
out four-source *terminal extremal* states, not four-source starting states.

The old four-source example is repaired, for instance, by replacing

    ({0,1},{2,3},{4,5},{6,7,8})

with

    ({1,2},{0,9},{4,5},{6,7,8}).

Both changing agents improve. Another example in the tests needs the triple
replacement branch, showing why compensation alone is not the whole proof.

## 3. Two-agent monotone repair is not universal

Consider the positive additive matrix below, with goods numbered 0,...,9:

    108   779     1    1     1    34    34    34    1    75
   4299  6461  3043   25  3393    50  3293  3093   25  3018
   1821     3   116  335   451     6   436    15   12     9
     56   329     2  335   357   297     8    58  331   363

Take

    A=({0},{1},{2,3,4},{5,6,7,8}),       g=9,
    Phi(A)=(v_0(A_0),v_1(A_1),v_2(A_2),v_3(A_3)).

A is EFX. Its envy edges are 0->1 and 2->0; its sources are agents 2 and 3.
For every pair of agents a,b, hold the other agents' bundles fixed and assign
each good in A_a union A_b union {g} to a, b, or the unallocated pool. This
includes arbitrary rebundling, changing the omitted good, and releasing several
goods; it is much broader than a swap or a one-good transfer.

Exact enumeration yields:

| Changing agents | All assignments | EFX strict lex improvements | Complete EFR |
| --- | ---: | ---: | ---: |
| 0,1 | 27 | 0 | 0 |
| 0,2 | 243 | 0 | 0 |
| 0,3 | 729 | 0 | 0 |
| 1,2 | 243 | 0 | 0 |
| 1,3 | 729 | 0 | 0 |
| 2,3 | 6561 | 0 | 0 |
| **Total** | **8532** | **0** | **0** |

The counts follow from 3^(|A_a|+|A_b|+1). Negative verdicts come from exhausting
these assignments with integer comparisons, not from a solver timeout.

### The obstruction is not caused by degeneracy

Define a second explicit instance by

    w_i(h)=112619 v_i(h)+1024*1[h in A_i]+2^h.

All 1024 subset values are distinct for each row. A remains EFX, and the same
8532-assignment enumeration again finds zero EFX lex improvements and zero
complete EFR outcomes. This preservation of the obstruction is **checked for
this instance**, not assumed from a general perturbation theorem.

Two independent enumeration implementations agree: one enumerates bitmask
subsets; the other uses Python sets, Cartesian products, and literal sums.
`verified-obstruction.json` records both the small base matrix and the explicit
nondegenerate matrix, verification counts, and escape witnesses.

Since the nondegenerate instance has no unchanged utility tuples for different
allocations, allowing neutral moves does not evade this obstruction. A path
whose every nontrivial EFX step changes at most two agents and never decreases
this fixed Phi cannot leave this start. A fixed priority chosen differently is
a different rule; we have not ruled out all priorities simultaneously.

### Three agents escape, and Mode C still succeeds

The partial allocation

    B=({5,9},{1},{0},{2,3,4})

is EFX and strictly increases Phi, for both the base and nondegenerate instances.
It changes agents 0,2,3 and leaves goods 6,7,8 unallocated. In the base instance,
own utilities change from (108,6461,902,694) to (109,6461,1821,694), a Pareto
improvement. In the nondegenerate instance, agent 3 loses 4548 utility units,
but agent 0 strictly improves, so the same fixed lexicographic potential rises.
BCFF restoration is now applicable.

There is also a complete EFR allocation holding agent 1 fixed:

    C=({0,2},{1},{3,4,5,6},{7,8,9}).

Finally, the exact unrestricted Mode C oracle finds this EFX predecessor:

    D=({1,4},{6,7,9},{0,3},{5,8}),       omitted good 2.

Adding good 2 to agent 2 gives EFR. These witnesses verify that the example
does not refute Mode C, let alone unrestricted EFR existence.

## 4. A three-agent compensated-path lemma

The escape above suggests a useful general sufficient condition. Choose distinct
agents s,i,t and h in A_t, with |A_t|>=2. Assume the pool bound v_j(g)<=u_j,

    v_i(g+h)>u_i,             v_s(A_i)>=u_s,

and let i precede t in the fixed agent priority. Set

    B_s=A_i,    B_i={g,h},    B_t=A_s,

leaving the fourth agent unchanged. Check only the donor's remaining EFX
inequalities:

    v_t(A_s)>=max_{j!=t, q in B_j} v_t(B_j minus {q}).            (5)

Empty targets impose no inequality. If (5) holds, B is EFX and Phi(B)>Phi(A).

**Proof.** Agents s and i weakly improve, with i strictly improving. The new
pair is safe at all old utility levels. Their comparisons, and the unchanged
agent's comparisons, against reused old bundles follow from original EFX;
comparison with an observer's former own bundle follows from nonnegativity.
Condition (5) checks the only agent who may lose utility. Since i precedes t
and nobody except t loses, the first changed coordinate is a gain. QED.

This lemma does not require an envy path from t to its champion i. It closes
the gap by giving t an old bundle from the other path, while explicitly checking
the fairness of a possible loss. For the example take (s,i,t,h)=(2,0,3,5).

The remaining proof obligation is to guarantee such compensation (or a broader
three/four-agent move) in every terminal configuration. The inequalities above
are sufficient conditions; we have not proved that they always hold.

## 5. Computer-checked structural exclusions

The compensation inequalities alone make 50 of the previous 156 extremal
regions infeasible. This includes 21 of the 24 (2,2,2,3) regions. In the last
three balanced regions, a finite menu of complete EFR allocations or EFX Pareto
improvements covers the region: respectively 41,30,30 menu entries for
2223_003, 2223_013, 2223_011. The final three searches use positive rows, which
suffice by the generic-counterexample reduction in STRUCTURAL_REDUCTIONS.md.

Every success clause is an exact conjunction of linear fairness inequalities,
and, for partial EFX moves, Pareto inequalities. Negating all success clauses
and all applicable elementary moves yields UNSAT. This is continuous-domain
coverage of the encoded region, not a finite sample argument.

Z3 generated the results. cvc5 1.4.0 independently returned UNSAT for all 54
original replay inputs, with proof generation and internal proof checking enabled.
The canonical evidence now retains 53 distinct inputs: the duplicate four-source
replay was removed during cleanup. All 53 distinct region results are preserved.
Portable inputs and SHA-256 hashes are generated by verify_two_source.py under
run/verification; canonical source evidence is retained separately.
The mathematical reduction and its Python encoding have not been verified in
a proof assistant; cross-solver checking does not remove that trust boundary.

| Profile | Previously remaining | After these checked exclusions |
| --- | ---: | ---: |
| (1,1,2,5) | 18 | 13 |
| (1,1,3,4) | 18 | 18 |
| (1,2,2,4) | 39 | 26 |
| (1,2,3,3) | 57 | 46 |
| (2,2,2,3) | 24 | 0 |
| **Total** | **156** | **103** |

The 103 unresolved regions have 94 two-source and 9 three-source templates.
No completion-time estimate or additional long GitHub workflow is claimed.
The old catalog remains available unchanged for reproduction of earlier runs.

## 6. What the attached monotone counterexample teaches us

The attached note's exponential amplification is outside the additive domain.
More strongly, even its strict pair ordering cannot be represented additively.
For agent 0, its B goods are 1,4 and C goods are 2,5. Its pair ranks require

    v({1,2})>v({1,4}),       v({4,5})>v({2,5}).

Additivity turns the first inequality into v(2)>v(4), and the second into
v(4)>v(2), a contradiction. Equivalently, additive values satisfy the exact
cancellation identity

    v({1,2})+v({4,5})=v({1,4})+v({2,5}).

Thus the useful inspiration is to search for a small structural obstruction
and certify it exactly, while imposing additive cancellation from the outset.
The note's high-ranked complementary pairs cannot be imported as additive
pair preferences.

## Reproduction

    python -m pip install -r requirements.txt
    python -m pip install cvc5==1.4.0
    python -m unittest -v test_two_source_moves test_structural_reductions
    python verify_two_source.py
    python verify_two_source.py --replay
    python two_source_probe.py --case 1134_041 --dominance lex --seconds 45

The final command is exploratory and may find a different model. The saved
verified obstruction and replay inputs are the reproducible statements. Probe
timeouts stay OPEN. No local obstruction is labeled as an EFR counterexample.

The next focused conjecture should allow at least three changing agents, or
permit a temporary fall in the chosen potential. For the finite-potential proof
route, a three-agent compensation lemma with conditions guaranteed on the 103
remaining templates is the more direct target.
