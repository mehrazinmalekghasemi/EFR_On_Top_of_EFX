# Dangerous items: a complete branch proof and a larger compensation move

**Superseding result:** [T11](FULL_STAR_AND_FAILURE_CASES.md#t11) now closes the
whole `1233_248` row, including the sole-champion/later-priority branch.
The 103-case counts and open-branch statements below record the earlier stage;
the current atlas has 102 open graphs.


Date: 2026-09-27. Four agents, ten goods, nonnegative additive valuations;
EFX means EFX0. This continues [SOURCE_COMPENSATION.md](SOURCE_COMPENSATION.md).

**New result:** the entire both-triples-champion-the-pair branch of
`1233_248` is excluded as a terminal extremal obstruction, for every fixed
agent priority. The constructive proof uses at most four changing agents;
it does not assert that four are necessary. The sole-champion/later-priority
branch remains open, so no whole graph row is removed from the 103-case atlas.

For two sources, a new three-agent theorem allows the donor to retain its
whole remainder. An explicit positive instance defeats every C1 compensation
proposal but satisfies this new theorem. Universal progress in all 94
two-source graphs is still unproved. No exhaustive valuation search was run.

## 1. Framework and elementary reductions

Write A_o={a}, A_p=P, A_q=Q, A_r=R, with sizes 1,2,3,3. In `1233_248`,
P,Q,R are unenvied sources and p,q,r all envy {a}. Thus, for every observer j,

    v_j(P), v_j(Q), v_j(R) <= u_j := v_j(A_j),
    v_k(a)>u_k for k=p,q,r.

Let z_j=v_j(g), and define R_j(S)=max_{h in S}v_j(S minus {h}), with the
empty-set value zero. A bundle is safe at the old utility levels when all
R_j(S)<=u_j.

We work after these existing elementary progress moves have been excluded:

(E1) z_j<=u_j for all j (otherwise the singleton {g} improves its recipient).

(E2) z_k+v_k(h)<=u_k for k=p,q,r and h in A_k (otherwise a self-pair improves).

(E3) z_o+v_o(h)<=u_o for h in P union Q union R (otherwise the source-to-o
path closes a safe-pair improvement).

(E4) Pair compensation is unavailable: if k=q or r champions h in P, meaning
z_k+v_k(h)>u_k, then v_p(y)<v_p(h) for every y in A_k.

All are necessary for a terminal extremal state, by earlier proved lemmas.
Every old item in P,Q,R is worth at most u_j to each observer j, by EFX and
nonnegativity. Therefore any pair of such items, or {g,h} with such an item,
is safe at the old utility levels. Old subbundles are safe as well.

Assume insertion into P is blocked. The singleton owner cannot block it under
(E3): all three two-good deletions from P+g are worth at most u_o. Hence q or r
blocks it. This gives at least one triple owner k with z_k>u_k/2, because

    2(v_k(P)+z_k)>3u_k,       v_k(P)<=u_k.

Throughout this note the agent priority is fixed. All moves in the first
proof are Pareto improvements and hence increase every fixed lexicographic
priority. The later residual-relay theorem explicitly checks priority.

## 2. The dangerous-item kernel

### D1. Failed replacements force exactly two dangerous items in each direction

Suppose both q and r champion an item of P. If an EFX triple replacement is
available, we already have Pareto progress. Otherwise

    u_q/2 < z_q <= 2u_q/3,       u_r/2 < z_r <= 2u_r/3,

and each of the sets

    D_q(R)={d in R : z_q+v_q(d)>u_q},
    D_r(Q)={c in Q : z_r+v_r(c)>u_r}

has exactly two elements.

**Proof.** By (E4), no Q item is dangerous for p: choose an item h of P
championed by q, and combine v_p(y)<v_p(h) with (E2). The same holds for R.
By (E3), no Q or R item is dangerous for o.

At least one triple owner is high-pool, as established above. For that owner,
replacing any item by g strictly improves utility, by (E2). The exact
replacement criterion S2 says failure of every replacement requires at least
two dangerous items for the other triple owner. Since the triple is unenvied,
this forces the other owner to have z>u/2. Apply the same argument in reverse.

Summing (E2) over a triple gives z<=2u/3. Three dangerous items in the other
source triple would have total value greater than 3(u-z)>=u, impossible for
an unenvied source. Thus there are exactly two in each direction. QED.

### D2. Exchanging dangerous items settles the two changing agents' EFX checks

Choose c in D_r(Q), d in D_q(R), and exchange them:

    Q'=(Q minus {c}) union {d},
    R'=(R minus {d}) union {c}.

Both owners strictly improve. Their EFX comparisons against every new bundle
hold automatically. Only unchanged agents o,p can block the exchange, and
they can do so only by envying a mixed pair consisting of one Q item and one
R item in a new triple.

**Proof.** For q,

    v_q(d)>u_q-z_q >= v_q(c),

so q improves; similarly r improves. Also, since R is unenvied and d is
dangerous to q,

    v_q(R minus {d}) < z_q.

A deletion from R' leaves either an old R subbundle, worth at most u_q, or c
and one remaining R item, worth less than (u_q-z_q)+z_q=u_q. The symmetric
argument handles r. The unchanged pair and singleton were already EFX targets.

For an unchanged observer, every unmixed pair is an old subbundle of Q or R
and worth at most its old utility. Thus any failure is a mixed pair. QED.

One useful sufficient condition falls out immediately: if all mixed Q/R
pairs are safe to both unchanged observers, any dangerous exchange works.
If q and r champion different items h,l of P, (E4) gives
v_p(x)+v_p(y)<v_p(h)+v_p(l)=u_p for x in Q,y in R. In that subcase p never
blocks. The next argument also handles the harder same-item subcase.

## 3. Repairing an external blocker

### D3. An envied mixed pair pays for a three-good compensation bundle

Orient Q,R so that an unchanged observer j in {o,p} envies a mixed pair

    E={t,d},       t in Q,       d in D_q(R),       v_j(E)>u_j.

Every failed exchange in D2 has such an orientation, possibly interchanging
q and r. There is a triple C subset of (Q minus {t}) union (R minus {d}) such
that

    v_r(C)>u_r,       R_q(C)<=u_q,       R_j(C)<=u_j.             (1)

**Construction and proof.** If t is dangerous to r, let y be the other of the
two dangerous Q items and set

    C={y} union (R minus {d}).

Then v_r(y)>u_r-z_r and v_r(R minus {d})>=z_r by (E2), so r strictly improves.

If t is not dangerous to r, keep both dangerous Q items y_1,y_2. Let e be an
r-most-valued item of R minus {d}, and set C={y_1,y_2,e}. Since
v_r(R minus {d})>=z_r, we have v_r(e)>=z_r/2. Consequently

    v_r(C)>2(u_r-z_r)+z_r/2=2u_r-3z_r/2 >= u_r,

where the last inequality uses z_r<=2u_r/3.

For q, an unmixed deletion pair is old and safe. A mixed deletion pair has a
Q item worth at most u_q-z_q and an R item worth less than z_q, because
v_q(R minus {d})<z_q. Thus C is safe to q at its old utility.

For j, each remaining Q item is worth at most u_j-v_j(t), and each remaining
R item at most u_j-v_j(d), because Q,R are unenvied. Every mixed pair in C
therefore has value at most

    2u_j-v_j(t)-v_j(d) < u_j.

Unmixed pairs are again old safe subbundles. This proves (1). C is disjoint
from E by construction. QED.

## 4. Complete proof of the both-champion branch

<a id="d4"></a>

### D4. Both triples championing the pair cannot be terminal

Under the assumptions in Section 1, suppose both q and r champion an item of
P. There is a partial EFX allocation that Pareto improves A.

**Proof.** Use a triple replacement if available. Otherwise D1 applies.
Try the dangerous exchange in D2. If it is EFX, we are done. Otherwise obtain
an external blocker j, orient Q,R as in D3, and construct E and C.
Let k be the other member of {o,p}.

If j=o, propose

    B_o=E,       B_q={a},       B_r=C,       B_p=P.

Agents o,q,r strictly improve. All new targets except C are safe at the old
utility levels. D3 makes C safe to o and q, and its recipient r improves.
Thus **the only possible failed EFX comparison is k=p against C**.

If j=p, choose h in P championed by q and propose

    B_p=E,       B_q={g,h},       B_r=C,       B_o={a}.

Agents p,q,r strictly improve. The same argument shows that **the only
possible failed comparison is k=o against C**. This is where both triples
being champions is useful: either orientation has an available h.

If the remaining comparison holds, this is the required three-agent Pareto
improvement. Otherwise k envies a two-good deletion F of C. F must be a mixed
Q/R pair, since unmixed pairs are old safe subbundles. In particular

    v_k(F)>u_k,       E intersect F is empty.

Now give E and F to their respective champions j,k. Give {a} to one triple
owner and {g,h} to the other, using an item h of P championed by that owner.
Both choices of triple owner are possible. Every agent strictly improves.

All allocated bundles have size at most two. E,F are pairs of old items from
nonsingleton bundles; {g,h} is safe by (E1); {a} is a singleton. Thus every
new target is safe at every old utility level. Strictly higher own utilities
imply EFX. The bundles are disjoint: E,F use only Q,R, while a,g,h are separate.
This is a four-agent Pareto improvement. QED.

This proof assigns g at most once. Unlike a naive champion-cycle rotation, it
never tries to give the same omitted good to several agents. It works for
zeros and ties; the strict inequalities used above come from blocking or envy.

The moves may leave several goods unallocated. Composing with the previously
established fixed-priority restoration theorem excludes terminal extremal
states. This does not prove that each intermediate move retains nine goods,
that three changing agents always suffice, or that the distance-five conjecture
holds. It also does not settle Mode C.

## 5. Two sources: a guaranteed residual relay

<a id="r1"></a>

### R1. Two singleton targets permit a larger donor remainder

Let s,i,t,r be distinct, with A_i and A_r singletons, |A_s|,|A_t|>=2. Suppose
A is EFX and the pool bound holds. Choose h in A_t such that

    v_i(g)+v_i(h)>u_i,          v_s(A_i)>=u_s,
    v_t(g)+v_t(h)<=u_t,        2v_t(h)<=u_t.                (2)

Set

    B_s=A_i,       B_i={g,h},       B_t=A_t minus {h},       B_r=A_r.

Then B is EFX. It improves the fixed lexicographic potential whenever a strict
gainer among s,i precedes t, or when v_t(h)=0.

**Proof.** Agent i improves and s weakly improves. The new pair is safe at the
old utility levels, and the donor's remainder is a safe old subbundle. The
only agent who may lose is t. Its comparisons against the two singleton
targets impose no requirement. Its comparison against {g,h} requires

    u_t-v_t(h) >= max(v_t(g),v_t(h)),

which is exactly guaranteed by (2). This proves EFX. The priority condition
ensures that a possible loss by t follows a strict gain. QED.

Unlike C1's two-good compensation class, the donor remainder may contain
three or four goods. Its EFX safety comes from being an old subbundle, not from
a bound on its cardinality. This is an additional move class.

The 13 open (1,1,2,5) and 18 open (1,1,3,4) graphs all have two singleton
nonsources and two nonsingleton sources, with at least one source-to-singleton
edge. Thus all 31 have the structural motif relevant to R1. **That does not
close those 31 cases:** a suitable champion h and the priority condition must
still be established, or an alternative move found.

On the previously verified two-agent obstruction, R1 with (s,i,t,h)=(2,0,3,5)
gives

    ({5,9},{1},{0},{6,7,8}),
    (108,6461,902,694) -> (109,6461,1821,397).

It is EFX and improves priority (0,1,2,3), also on the saved nondegenerate
refinement. No search over compensation bundles is needed for this witness.

### R2. What failure of an enlarged compensation menu actually implies

For an eligible C1 relay with T={g,h}, let H=A_s union (A_t minus {h}). In
addition to its best two-good subset, two safe compensation candidates are
A_s and A_t minus {h}. Write

    M_t = max(v_t(top-two(H)), v_t(A_s), u_t-v_t(h)),
    L_t = max(v_t(g),v_t(h),R_t(A_i),R_t(A_r)).

Every candidate is safe at old utility levels. If a strict gainer precedes t,
M_t>=L_t suffices for a valid relay. Under the two donor inequalities in (2),
failure therefore forces

    max(R_t(A_i),R_t(A_r)) > M_t.                         (3)

**Proof.** The remainder alone covers max(v_t(g),v_t(h)); hence that part of
L_t cannot cause the deficit. One of the old targets must cause it. QED.

When both old targets are singletons, (3) is impossible. This recovers R1.
For an eligible two-singleton relay with an earlier strict gainer and the
self-pair bound, failure of even the remainder move forces the donated good
to be dominant:

    v_t(h)>u_t/2.

For other profiles, (3) identifies a specific large deletion value that a
broader repair must remove or compensate. If the donor precedes all strict
gainers, full recovery of u_t is instead required; that is a distinct priority
obstruction. If no eligible relay exists, no threshold-deficit argument applies.
These distinctions are essential when formulating a universal disjunction.

## 6. Exact counterexample to C1 alone, with a proved escape

Take the saved two-agent-obstruction matrix from
[TWO_SOURCE_PROGRESS.md](../TWO_SOURCE_PROGRESS.md), changing only its last row to

    56 329 100 100 100 200 120 120 120 350.

Keep A=({0},{1},{2,3,4},{5,6,7,8}), g=9, and priority (0,1,2,3). This is EFX
with two sources. **Every C1 proposal fails**, even allowing all subsets T of
A_t union {g}, not merely pairs.

Here is a direct proof. The only eligible nonsingleton path-start s is agent 2,
and the only old bundle it weakly prefers is A_0; the donor is therefore 3.
Agent 0 values g at 75 and donor goods at 34,34,34,1. A safe champion T cannot
have at least three items and contain a 34-valued item: deleting another item
would leave value at least 75+34=109>108. Thus the only safe champion bundles
are {g,5}, {g,6}, {g,7}.

For h=5, the top-two compensation value is 240; for h=6 or 7 it is 320.
The donor's EFX floor is 350 in each case. All C1 proposals fail independently
of priority. Exact checking of all 168 ordered proposals confirms this.

But R1 applies with h=5:

    v_3(h)=200 <= 560/2,       v_3(g)+v_3(h)=550 <= 560.

The donor retains three goods worth 360, meeting the 350 fairness floor.
The resulting own utilities are

    (108,6461,902,560) -> (109,6461,1821,360).

This is EFX and strictly improves the fixed potential. The example refutes
universal coverage by C1's two-good compensation class; it is not a
counterexample to broader three-agent progress, Mode C, or EFR existence.

A separate saved (1,2,3,3) example in `1233_241` has no eligible successful C1
relay at all, all four immediate insertions fail, and no reachable safe
champion exists, yet an explicit complete EFX allocation Pareto improves it.
That example illustrates failure of relay eligibility rather than a numeric
compensation deficit. The two phenomena are deliberately distinguished.

## 7. Remaining proof obligations and next steps

| Region or assertion | Status |
| --- | --- |
| `1233_248`, both triples champion P | **Proved: D4**, all fixed priorities |
| `1233_248`, sole champion precedes other triple | **Proved: S3** in the previous note |
| `1233_248`, sole champion follows other triple | **OPEN** |
| Other eight three-source graph rows | **OPEN** as whole rows |
| Eligible two-singleton relay satisfying (2) and priority condition | **Proved: R1** |
| Universal C1 compensation | **False**, Section 6 |
| Universal three-agent progress for all 94 two-source graphs | **OPEN** |
| Unrestricted EFR existence / Mode C / distance-five escape | **OPEN** |

Next theoretical targets:

1. Extend the mixed-pair repair argument to the sole-champion/later-priority
   branch. In D4 either orientation could obtain {g,h}; with a sole champion
   that symmetry disappears. This is now the precise missing resource.
2. For the 31 two-singleton graph templates, separate absence of a champion,
   an earlier donor, and a dominant donated item. R1 settles the other
   eligible subregion without searching valuations.
3. For the remaining two-source profiles, use (3) to locate the obstructing
   old target, then attempt a dangerous-item exchange or a larger safe
   remainder. Prove a disjunction of moves, not a universal C1 claim already
   refuted by an explicit instance.
4. Keep priority attached to physical agents for R1 and any lossy moves. D4's
   Pareto argument needs no priority-dependent symmetry split.

## 8. Implementation and verification

`efr/dangerous_moves.py` implements the D4 construction and R1, checking their
stated assumptions. It neither implements BCFF restoration nor launches a
valuation search. Evidence is in
[experiment-results/dangerous-items/witnesses.json](../experiment-results/dangerous-items/witnesses.json).

The saved witnesses exercise triple replacement, dangerous exchange, a
singleton blocker, a pair-owner blocker, and the disjoint-pair four-agent
fallback. Independent set-and-sum tests verify EFX, disjointness, and Pareto
improvement under all 24 simultaneous agent relabelings. They also check the
C1 counterexamples and fixed-priority residual escapes. These tests support
the implementation; the universal branch claim rests on the proof above.

    python -m unittest -v tests.test_dangerous_moves
    python -m unittest discover -v
    python -m efr.case_status --check

The atlas's whole-graph counts remain unchanged. No SMT coverage campaign or
new exhaustive valuation search was launched.
