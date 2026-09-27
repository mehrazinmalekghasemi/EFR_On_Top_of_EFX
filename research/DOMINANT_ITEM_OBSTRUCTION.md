# Dominant donated items: exact thresholds and blocker rerouting

Date: 2026-09-28 (Tehran). Nonnegative additive valuations, four agents,
ten goods, EFX0. Continuation of
[FULL_STAR_AND_FAILURE_CASES.md](FULL_STAR_AND_FAILURE_CASES.md#8-two-source-failure-type-f3-a-dominant-donated-item).

**New results:** a complete reduction of a fixed dominant-item relay to at most
20 minimal compensation candidates; a proved rerouting move when a candidate
is blocked; and explicit examples showing that the total compensation budget
alone is insufficient, in both priority branches. These are local theorems.
The case atlas remains **102 open graph templates (94 two-source, 8 three-source)**.
No new whole graph is closed, and no exhaustive valuation campaign was run.

## 1. Fix the allocation and the priority once

Let A_i={a}, A_r={b}, S=A_s and A_t={h} union D, with |S|,|A_t|>=2.
The omitted good is g. Write u_j=v_j(A_j), z_j=v_j(g), and

    R_j(X)=max_{x in X} v_j(X minus {x}),    R_j(empty)=0.

Assume A is EFX, z_j<=u_j for every j, and

    v_s(a)>=u_s,             v_i(g+h)>u_i,
    alpha:=v_t(h)>u_t/2,     z_t+alpha<=u_t.

These are the eligible relay and dominant-item hypotheses. In the intended
application S and A_t are the two sources, but the following local proofs do
not require their source property. Put d=v_t(D)=u_t-alpha. Then

    z_t<=d<alpha.

The priority pi is an order of the physical agent identities. Keep it fixed.
Let G consist of i, and also s if v_s(a)>u_s.

- **Later-loss branch:** some agent in G precedes t. Set L=alpha.
- **Full-recovery branch:** t precedes every agent in G. Set L=u_t.

A donor merely preceding i is not sufficient to select the second branch.
For compensation C subset of H=S union D, consider

    B_s={a},    B_i={g,h},    B_t=C,    B_r={b}.            (1)

There are exactly six goods in H, since the other two old bundles are
singletons and h has been removed from the seven source goods.

## 2. D12: an exact threshold and at most 20 candidates

Define the provisional utilities of the three observers by

    w_s=v_s(a),    w_i=v_i(g+h),    w_r=u_r.

**Theorem D12.** Allocation (1) is EFX and strictly improves pi if and only if

    v_t(C)>=L,       R_j(C)<=w_j for j in {s,i,r}.          (2)

It suffices to examine inclusion-minimal subsets C satisfying v_t(C)>=L.
There are at most 20 such subsets of H.

**Proof.** Every old good in a nonsingleton bundle is worth at most u_j to
an external observer j, by EFX and nonnegativity; to its owner it is bounded
by its old bundle value. Thus {g,h} is safe at all old utility levels.
The three observers weakly improve, and i strictly improves. Their only
possibly unsafe target is C. The donor's only nonsingleton other target is
{g,h}, imposing exactly max(z_t,alpha)=alpha. If a strict gain precedes t,
that floor suffices for lexicographic progress. Otherwise t must recover u_t;
if it recovers exactly, i supplies a later strict gain. This proves (2).

For nonnegative additive values, R_j is monotone under set inclusion. Indeed,
for X subset Y and x in X, v_j(X minus {x})<=v_j(Y minus {x})<=R_j(Y).
Therefore shrinking a feasible compensation to a minimal threshold cover
preserves all three safety inequalities. Conversely, any such safe minimal
cover is itself a feasible compensation.

The minimal covers form an antichain: none contains another. For a uniform
random ordering of the six goods, the event that a fixed k-element cover is
the first k goods has probability 1/binom(6,k). Two different antichain
members cannot both be initial segments of the same ordering. Hence

    sum_C 1/binom(6,|C|) <= 1.

Since binom(6,k)<=20, their number is at most 20. QED.

The total-value necessary conditions become

    v_t(S)>=alpha-d       [later loss],
    v_t(S)>=alpha         [full recovery].                (3)

These are not sufficient: observer safety remains essential. Section 5 gives
counterexamples even when (3) holds with equality.

This reduces *expensive compensation safety checks* from 64 possible subsets
to at most 20 minimal candidates. The implementation still constructs the
small subset list to identify them. It does not reduce the continuous valuation
domain to 20 points, nor justify a factor-3 runtime prediction for the global
search. The 20 bound concerns compensation candidates, not all auxiliary
subsets examined in the rerouting step.

## 3. D13: a blocking subset can reroute the relay

Let C be a minimal threshold cover. If it is unsafe in (2), some proper subset
of C is envied by an observer at the provisional utility w_j. Choose E that
is inclusion-minimal among subsets envied by **any** of the three observers.
Choose any observer j with v_j(E)>w_j. Global minimality, rather than minimality
only for j, is essential. Define the provisional target bundles

    K_s={a},    K_i={g,h},    K_r={b}.

**Theorem D13.** If v_t(K_j)>=L, give E to j and K_j to t, leaving the other
two provisional bundles unchanged. This is an EFX allocation strictly
improving the same fixed priority.

**Proof.** Every deletion of E is unenvied by all three observers, by its
minimality. Thus E is safe at their provisional utility levels. Agent j
strictly improves over w_j, and the other two observers retain their w values.
The displaced bundle K_j is either a singleton or the safe pair {g,h}, so it
causes no EFX violation for any of these observers.

Since C is a minimal threshold cover and E is a proper subset,

    v_t(E)<L<=v_t(K_j).

Consequently the donor does not even envy E. Any remaining singleton target
has deletion value zero; the only possible remaining pair {g,h} has deletion
value alpha<=L. The donor's EFX comparisons therefore all hold. Disjointness
follows from E subset H and K_s,K_i,K_r being mutually disjoint and outside H.

All old strict gainers in G remain strict gainers. In the later-loss branch
one still precedes the donor; in the full-recovery branch the donor recovers.
The fixed lexicographic potential strictly increases. QED.

**Consequences.**

1. In the later-loss branch, a minimal blocking subset championed by i is
   always repairable: v_t(K_i)=alpha+z_t>=L=alpha. The donor keeps {g,h},
   while i takes E. If no such rerouting works, every minimal blocking subset
   can only be championed by s or r, and each champion's displaced singleton
   is worth less than alpha to t.
2. In the full-recovery branch, rerouting to i works exactly at the self-pair
   boundary z_t=d; otherwise alpha+z_t<u_t. Rerouting via s or r requires
   its displaced singleton to be worth at least u_t to the donor.
3. Later loss admits a sufficient budget theorem: if v_t(H)>=alpha and both
   v_t(a),v_t(b)>=alpha, then a safe compensation or D13 repair always exists.
   Every possible minimal blocker is repairable.
4. Similarly, full recovery is guaranteed when v_t(H)>=u_t, z_t=d, and both
   singleton values to t are at least u_t.

These conditions are sufficient, not necessary. A low-valued displaced bundle
only rules out this particular rerouting; a different compensation or broader
move may still succeed.

## 4. What is left after all these moves fail?

For a fixed eligible relay:

| Branch | Necessary residual obstruction |
| --- | --- |
| Either branch, v_t(H)<L | Insufficient total budget for this relay |
| Later loss, v_t(H)>=alpha | Every minimal cover is unsafe; all its globally minimal blocking subsets have only low-valued singleton blockers |
| Full recovery, v_t(H)>=u_t | Every minimal cover is unsafe; every minimal blocker's displaced bundle has donor value below u_t |

Here a "low-valued singleton blocker" is s or r whose provisional singleton
has donor value below L, not a statement that the singleton is low-valued to
its current owner. The distinction between valuations is essential.

This is a universal disjunction *within the fixed relay*, proved by D12–D13.
It does not claim that the remaining row is impossible. The examples below
show it can occur even when both sources and all four blocked insertions are
present.

## 5. Two explicit budget counterexamples, both with complete EFX escapes

Use goods 0,...,9, omitted g=9, and

    A_i={0}, A_r={1}, S={2,3,4}, A_t={5,6,7,8}, h=5.

Agents are ordered (i,r,s,t)=(0,1,2,3). Take

| Agent / good | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| i | 10 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 7 |
| r | 0 | 3 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 2 |
| s | 5 | 5 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 2 |
| t | 0 | 0 | x | x | x | 18 | 4 | 4 | 4 | 3 |

For **later loss**, set x=2 and pi=(0,1,2,3). For **full recovery**, set x=6
and pi=(3,0,1,2). In both cases:

- A is EFX; S,A_t are exactly the two sources. The strict envy edges are s->i
  and s->r.
- All four immediate EFR insertions fail. Agent s blocks insertion into either
  singleton: (5+2)/2>3. Agent r blocks insertion into S and A_t: respectively
  3(3+2)/4>3 and 4(3+2)/5>3.
- The only item in A_t forming a champion pair with g for i is h=5.
- u_t=30, alpha=18, d=12, z_t=3. All pool and source self-pair bounds hold.
- H={2,3,4,6,7,8} has donor value exactly L: 18 in the later-loss example and
  30 in the full-recovery example. Every H item has strictly positive donor
  value, so the only threshold cover is H itself.
- Agent r values H at 6 and every five-item deletion at 5>u_r=3. Consequently
  **no compensation subset whatsoever makes this fixed relay work**.
- Every minimal blocking subset has four goods and is championed only by r.
  Its displaced singleton {1} is worth zero to t, so D13 cannot repair it.

These refute the tempting claim "the total budget inequality guarantees a
compensation", for both priorities. They do not refute general progress.
Indeed, both have the complete EFX Pareto improvement

    B_i={0,9}, B_r={2,3,4}, B_s={1}, B_t={5,6,7,8}.

Own utilities change from (10,3,3,30) to (17,3,5,30). The donor keeps its
entire old bundle. This escape exchanges the singleton owner r with source s
and then inserts g at i, rather than donating the dominant item.

The examples use zeros and ties and make no nondegeneracy claim. They are
exact counterexamples within the requested nonnegative additive domain.

## 6. Next proof target: reroute the singleton ownership

The surviving later-loss obstruction is now about a **singleton owner**, not
the intended champion. The examples suggest a second family of moves.

A simple conditional escape is already rigorous. If

    v_s(b)>=u_s,       v_r(S)>=u_r,

swap S and {b} between s and r. This is a partial EFX Pareto nondecrease:
the target bundles are old EFX bundles, and no agent loses utility. If one
inequality is strict, it is a Pareto improvement without using g. Whether or
not the swap is strict, test insertion of g into {a} at i using the exact EFR
criterion; if it succeeds, we have a complete EFR allocation. It succeeds
in both examples above (indeed the outcome is complete EFX).

Failure of this escape supplies an explicit further disjunction: s does not
accept b, r does not accept S, or insertion remains blocked after the swap.
However, the minimal-blocker inequalities do **not yet prove** that one of
these singleton swaps or a longer rotation must succeed. That is the next
useful theoretical obligation, before a broad continuous search.

For full recovery away from z_t=d, there is a second deficit to address even
if i is the blocker: the donor keeping {g,h} is short by d-z_t. One possible
extension is to add a released good or safe subset worth at least d-z_t to
the donor. The resulting larger donor bundle must be checked against every
observer; no guaranteed topping-up theorem is asserted.

## 7. Code and verification scope

`efr/dominant.py` implements D12–D13 with exact rational arithmetic and explicit
priority. `None` means no move from these specified classes for the supplied
relay, not a global impossibility. Evidence is stored in
[dominant-item-witnesses.json](../experiment-results/dangerous-items/dominant-item-witnesses.json).
Tests independently check EFX and fixed-priority progress, all 24 simultaneous
agent relabelings, both budget counterexamples, and complete EFX escapes.

    python -m unittest -v tests.test_dominant

No existing atlas cell is relabeled and no historical solver certificate is
changed. The current proof does not establish a universal three-agent repair,
Mode C, unrestricted EFR existence, or the distance-five escape conjecture.
