# Singleton blockers and safe recovery of the donor deficit

Date: 2026-09-28 (Tehran). Four agents, ten goods, nonnegative additive values,
EFX0. Continues [D12–D13](DOMINANT_ITEM_OBSTRUCTION.md).

**Results:** D14 repairs some previously unresolved singleton blockers and early
donors by augmenting the displaced bundle. D15 gives exact safety inequalities:
the blocker’s utility surplus must cover the value of every top-up deletion.
A counterexample shows that ample leftover value need not meet these constraints.
The whole-case count stays 102 (94 two-source, 8 three-source). These theorems
concern specified local moves; no universal repair theorem is claimed.

## 1. Setup and a necessary priority refinement

Use the earlier notation A_i={a}, A_r={b}, A_s=S, A_t={h} union D,
g omitted, u_j=v_j(A_j), alpha=v_t(h)>u_t/2, d=v_t(D), z_t=v_t(g)<=d.
The eligible relay has provisional observer bundles

    K_s={a}, K_i={g,h}, K_r={b},

with w_s>=u_s, w_i>u_i, w_r=u_r. Let H=S union D. Choose a minimal donor
threshold cover C and a proper E subset C that is inclusion-minimal among
subsets envied by any observer at these provisional utility levels. Let j be
a champion: v_j(E)>w_j. D13 fails when K_j is too cheap for the donor.

Give E to j and retain K_k for the other two observers. Let these three
observer bundles be B_k and their values be W_k=v_k(B_k). The donor can receive

    Q=K_j union F,       F subset H minus E.               (1)

**Keep the same physical priority pi.** Recompute the strict gainers after
j receives E. If j was previously unchanged, it is now an additional gainer.
An apparently early donor can therefore become allowed to lose without any
change of priority. No identity or priority is relabeled to manufacture progress.

Define

    q=max_{k!=t} R_t(B_k),
    L'=q                      if some strict gainer precedes t,
    L'=max(q,u_t)             otherwise,
    delta=max(0,L'-v_t(K_j)).                              (2)

When j=i and the donor must still recover, q<u_t because E is a proper subset
of a minimal u_t-cover, and the other targets are singletons. Hence

    delta=u_t-v_t(g+h)=d-z_t.                              (3)

For a singleton blocker, the remaining champion pair still contributes alpha
to q. A blocker originating from a full-recovery cover can contribute a larger
R_t(E), so blindly keeping the old later-loss floor alpha is not always valid.

## 2. D14: exact augmentation theorem

**Theorem.** The allocation described in (1) is EFX and improves pi exactly when

    v_t(F)>=delta,
    R_k(K_j union F)<=W_k for every k!=t.                  (4)

It suffices to check inclusion-minimal top-ups meeting the first inequality.
There are at most six such candidates for each E,j.

**Proof.** Global minimality of E makes each deletion of E worth at most w_k
to every observer k. Each observer now has at least w_k; all other observer
targets are unchanged safe pairs or singletons. Thus the only remaining
observer checks are the three inequalities in (4). The donor’s exact EFX
floor is q. The fixed-priority comparison gives the two alternatives in (2),
since at least the original champion i remains a strict gainer. This proves
necessity and sufficiency.

Shrinking a top-up while retaining its donor threshold can only reduce every
observer’s deletion value. Therefore a successful top-up has a successful
minimal sub-top-up.

Every good in H came from an old nonsingleton bundle and is worth at most u_k
to any observer k. Since w_k>=u_k, no singleton subset of H is envied at w_k.
Thus |E|>=2 and |H minus E|<=4. Minimal threshold covers form an antichain,
so the same initial-segment counting argument as D12 bounds their number by
binom(4,2)=6. If delta=0, the empty set is the sole minimal top-up. QED.

The implementation only applies this theorem to blockers produced by D12–D13.
If the original cover family is empty, it does not claim to have tested every
other possible way to produce a blocking subset or change the allocation.

## 3. D15: the blocker's surplus is the precise safety resource

For nonempty disjoint K,F, additivity gives the exact identity

    R_k(K union F)=max(R_k(K)+v_k(F), v_k(K)+R_k(F)).       (5)

The two terms correspond to deleting an item from K and from F, respectively.
When F is empty use R_k(K) directly.

Let epsilon=v_j(E)-v_j(K_j)>0 be the blocker’s gain beyond its provisional
utility. Its own check against the augmented donor bundle is equivalent to

    R_j(F)<=epsilon,
    v_j(F)<=v_j(E)-R_j(K_j).                              (6)

These are not merely necessary approximations: together they are exactly that
observer’s EFX constraint. The other two observers have the corresponding
bounds from (5) at their W levels.

For a singleton displaced bundle K_j={x}, (6) becomes

    R_j(F)<=epsilon,       v_j(F)<=v_j(E).

For an early donor receiving K_i={g,h}, the sought resource is therefore a
subset F worth at least d-z_t to t while meeting (5) for all observers. Large
aggregate donor value alone cannot establish that such an F exists.

## 4. Explicit repairs of cheap singleton blockers

Use A=({0},{1},{2,3,4},{5,6,7,8}), g=9, h=5 and (i,r,s,t)=(0,1,2,3).
The first three rows are

    i: 10 13 0 0 0 5 0 0 0 8
    r:  0  3 1 1 1 0 1 1 1 2
    s:  5  0 1 1 1 0 0 0 0 2

For later loss, use

    t:  0 12 3 3 3 18 3 3 3 3,    pi=(0,1,2,3).

For full recovery, use

    t:  0 24 6 6 6 18 4 4 4 3,    pi=(3,0,1,2).

Both initial allocations are EFX with exactly two sources, and all four
immediate EFR insertions fail. The simple swap s<-{1}, r<-S is unavailable:
v_s({1})=0<u_s=3. D12–D13 also return no move.

For both, choose the singleton blocker r and E={2,3,4,6}, whose value to r is
4>3. Its displaced singleton is {1}. Let F={7,8}. The resulting allocation is

    B_i={5,9}, B_r={2,3,4,6}, B_s={0}, B_t={1,7,8}.

This is complete EFX. Utilities are

    later: (10,3,3,27) -> (13,4,5,18),
    early: (10,3,3,30) -> (13,4,5,32).

The later donor loses only after a fixed-priority gain. The early donor fully
recovers and strictly gains. In both cases the singleton alone misses the
required threshold by six, and the top-up supplies six or eight respectively.
The blocker's surplus is epsilon=1; the two top-up items are each worth one
to it, so R_r(F)=1 meets (6) exactly.

## 5. Early champion blocker: a repair and a sharp safety obstruction

Keep the same A,g,h and pi=(3,0,1,2). Use

    i: 10 0 6 y y 4 6 0 0 7
    r:  0 3 0 0 0 0 0 0 0 2
    s:  5 5 1 1 1 0 0 0 0 2
    t:  0 0 6 6 6 18 4 4 4 3.

For y=0, D12–D13 fail. The unique minimal envied subset is E={2,6},
championed by i, with value 12>v_i(g+h)=11. The donor receives {g,h} plus
F={3,4}, worth 12 to it. This covers the deficit d-z_t=12-3=9.
The partial EFX Pareto improvement is

    B_i={2,6}, B_r={1}, B_s={0}, B_t={3,4,5,9},
    (10,3,3,30) -> (12,3,5,33).

For **y=2**, the same E remains the unique minimal blocking subset, but no
augmentation works. There are 20 units of donor value in H minus E, more than
the required nine. Nevertheless:

- every single leftover item is worth at most six to t, so at least two are
  needed;
- the two leftover D items together are worth only eight, so F must contain
  one of goods 3,4, each worth two to i;
- any such multi-item F has R_i(F)>=2, but the blocker's surplus is only
  epsilon=12-11=1.

Equation (6) rules out **every top-up**, not just the five minimal candidates
explicitly checked by the implementation. The matrix still has two source
bundles. This example is a counterexample to sufficiency of leftover value,
not to unrestricted repair or EFR existence.

For avoidance of doubt, an independently checked Mode C witness is

    omitted 7, predecessor ({6,8,9},{1,3},{0,2},{4,5}),
    insert 7 into agent 2's bundle.

The resulting complete allocation is EFR. Thus this local obstruction is
compatible with the project's desired global construction.

## 6. What must be proved next

The right next obligation has two numerical sides: the donor's deficit and
the blocker's surplus. A useful candidate disjunction is:

    a safe top-up satisfying (4), OR a different rotation/rebundling that
    changes the blocker or increases its surplus.

The second alternative remains unproved. The y=2 example shows that one cannot
simply argue that enough released value forces a safe top-up. Any universal
proof must change the bundle assignment or the blocking subset in this branch.
Likewise, some cheap-singleton blockers have too little leftover donor value
and need a different move altogether.

No graph row is removed from the open atlas. The new implementation enumerates
only small subsets for a supplied instance; it is not a continuous exhaustive
search or a runtime estimate for the global problem.

## 7. Evidence

Code: `efr/dominant.py`, function `augment_dominant_blockers`.
Tests: `tests/test_dominant_top_up.py`.
Examples: [singleton-top-up-witnesses.json](../experiment-results/dangerous-items/singleton-top-up-witnesses.json).
The tests independently check all proposed allocations, all 24 simultaneous
agent relabelings with priority preserved, and every one of the 16 possible
top-up subsets in the safety counterexample.
