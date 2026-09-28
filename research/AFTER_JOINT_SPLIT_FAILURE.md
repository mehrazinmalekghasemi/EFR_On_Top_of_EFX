# After every joint split fails: the 31 two-singleton cases

Date: 2026-09-28 (Tehran). Nonnegative additive valuations; EFX0. The priority
is fixed throughout. This note concerns only (1,1,2,5) and (1,1,3,4).

**Main advance:** a dominant-donor terminal branch is impossible in six of the
13 (1,1,2,5) templates when the pair source reaches both singleton owners.
For eleven of the 18 (1,1,3,4) templates the same reachability gives a precise
one-item replacement obstruction. A different singleton rotation also repairs
examples where every recorded joint split fails. No whole template is closed.

## 1. Why the fixed joint split can genuinely fail

Use A_i={a}, A_r={b}, A_s=S, A_t={h} union D, H=S union D. Suppose a singleton
blocker j receives E union X, while the donor receives K_j union F, as in D16.
Necessarily

    v_t(K_j union F) <= v_t(K_j)+v_t(H)-v_t(E).

If i keeps {g,h}, the donor must still meet the EFX floor alpha=v_t(h).
Consequently, when v_t(H)=alpha, v_t(K_j)=0 and v_t(E)>0, **no joint split**
can work in the later-loss branch. If the donor is first in priority, replace
alpha by u_t to obtain the analogous full-recovery obstruction. This is a
budget proof covering all splits, independent of how much surplus j gains.

Thus one cannot prove universal progress while insisting on the same two
provisional singleton/champion assignments. At least one of them must change
in this class. This does not rule out a different relay, source replacement,
EFR insertion, or a broader rearrangement.

## 2. D19: reachability rules out the dominant branch for a pair source

Let S be an unenvied pair source and T the other, five-good source. Suppose
both singleton owners are reachable from S in the strict envy graph. Assume
the pool bounds v_j(g)<=u_j and

    v_t(g)<=u_t/2.                                      (1)

**Theorem D19.** Either inserting g into S is EFR, or there is a partial EFX
Pareto improvement. This holds for every fixed priority.

**Proof.** A self-pair {g,x}, x in S, preferred by s already gives a safe
Pareto improvement: all its singleton deletions are bounded by old utilities.
Otherwise consider insertion into S. The observer condition is

    2(v_j(S)+v_j(g)) <= 3u_j.

Agent t satisfies it, since S is unenvied and (1) holds. If insertion fails,
a singleton owner j blocks it. Since v_j(S)<=u_j, failure implies some x in S
satisfies v_j(g+x)>u_j. Indeed, if both pairs were unenvied, adding their
inequalities and the source bound would give 2(v_j(S)+v_j(g))<=3u_j.

Every pair {g,x} is safe at old utility levels: g satisfies the pool bound and
x comes from an old nonsingleton bundle. Rotate old bundles along a strict envy
path from s to j, and give {g,x} to j. No other source can lie on this path,
since it has no incoming envy edge. All path agents strictly improve; all
unchanged agents retain their utilities. The rotated old singleton bundles
and the new pair are safe. The allocation is disjoint and EFX. QED.

**Dominant-item consequence.** After excluding self-pair improvements of t,
any item h in T with v_t(h)>u_t/2 implies

    v_t(g)<=u_t-v_t(h)<u_t/2.

Therefore a terminal state under D19's reachability hypotheses cannot have a
dominant item at t. This proves an alternative even if every joint split fails;
no compensation threshold or priority loss is needed.

The six affected graph templates are

    1125_041, 1125_0c1, 1125_4c1,
    1125_441, 1125_0c0, 1125_2c0.

Only their stated valuation subregions are eliminated. The templates remain
OPEN because their other-source pool value may exceed u_t/2 and they need
not have a dominant donated item. The other seven pair-source templates
lack the required reachability and are not covered by this theorem.

## 3. D20: the corresponding triple source has at most one dangerous item

Now S has three goods and T has four. Both singleton owners are reachable
from s. Exclude pool improvements and reachable safe-pair improvements. Then

    v_j(g)+v_j(x)<=u_j

for each singleton observer j and every x in S; otherwise the same path
rotation used in D19 is an improvement.

Assume t has a dominant item and its self-pair cut, so z_t<u_t/2. Since S is
unenvied, at most one item x in S can satisfy

    z_t+v_t(x)>u_t.                                     (2)

Two such items would together be worth more than u_t to t, contradicting
v_t(S)<=u_t.

**Theorem D20.** If there is one dangerous item x in (2), replacing x by g
is EFX and strictly improves s whenever z_s>v_s(x). If there is none,
replacing a least-valued item of S is EFX and strictly improves s whenever
z_s>min_{y in S} v_s(y).

**Proof.** Deleting g leaves an old source pair. Every other deletion leaves
g and one retained item. The singleton observers satisfy the reachable-pair
cuts, and t satisfies them after the unique dangerous item, if any, is removed.
The source owner improves, so its old-target comparisons remain valid. QED.

Thus failure forces either

    unique dangerous x and z_s<=v_s(x),

or no dangerous item and z_s<=min_{y in S}v_s(y). In particular, under s's
self-pair cuts a terminal state must have z_s<=u_s/2: if z_s>u_s/2, every
source item is worth at most u_s-z_s<z_s, making the prescribed removal
profitable. This is a concrete remaining inequality, not a universal closure.

The eleven reachability templates are

    1134_041, 1134_0c1, 1134_2c1, 1134_6c1, 1134_4c1,
    1134_241, 1134_641, 1134_441, 1134_0c0, 1134_2c0, 1134_6c0.

The other seven triple-source templates require another strategy.

## 4. A different assignment: retain the donor's dominant item

When the compensation frame fails, consider instead

    B_i={a,g}, B_s={b}, B_r=E, B_t=(S union T) minus E,

where E excludes h, so t retains its dominant item. This changes both the
location of g and the singleton assignment. Require s and r not to lose;
the donor's potential loss is allowed only after an earlier strict gain.

For each proposed E, the only nontrivial comparisons are against {a,g}, E,
and the donor's new bundle. Checking these exactly is essential: the old
singleton a need not be individually safe to other agents at their old values.
There are only 64 complete redistributions of the six source goods other than
h. The routine certifies a successful move but makes no global claim on failure.

Here are two examples where *every D16 joint split fails*, but this new frame
has a complete EFX escape. Use A=({0},{1},{2,3,4},{5,6,7,8}), g=9, h=5 and

    i: 10 0 0 0 0 4 0 0 0 7
    r:  0 4 1 1 1 0 1 1 1 3
    s:  5 5 1 1 1 0 0 0 0 2
    t:  0 0 x x x 18 4 4 4 3.

For x=2 and priority (0,1,2,3), use

    ({0,9}, {2,3,4,6}, {1}, {5,7,8}),
    (10,4,3,30) -> (17,4,5,26).

For x=6 and priority (3,0,1,2), use

    ({0,9}, {2,6,7,8}, {1}, {3,4,5}),
    (10,4,3,30) -> (17,4,5,30).

In both, all four immediate insertions fail. H has donor value exactly the
required D12 threshold (18 or 30); every minimal blocking subset is championed
only by r, contains five goods, and has positive donor value. Its displaced
singleton is worth zero to t. The budget argument in Section 1 excludes all
joint splits, even after enlarging the blocker. The simple old-bundle swap
also fails because v_r(S)=3<4.

These are witnesses to the limitation of the joint-split class, **not terminal
obstructions**: they also admit a simpler source triple replacement by D20.
This distinction is important. We must apply structural reductions before
spending effort searching difficult-looking compensation examples.

## 5. Next proof obligations, now separated

| Region within the 31 cases | Next obligation |
| --- | --- |
| Six reachable pair-source templates, dominant donor | Settled by D19 under the elementary cuts |
| Eleven reachable triple-source templates, dominant donor | Handle the remaining low-z_s or expensive forced-removal branch from D20 |
| Seven pair-source and seven triple-source templates with missing reachability | Use the singleton outside s's reachability component; establish a cross-component move |
| No dominant eligible donor / no eligible pair relay | Outside the dominant-item analysis; still part of the original 31 cases |

The most focused next task is the triple-source branch where the unique
item dangerous to t costs s at least z_s. The donor values that item highly,
which suggests exchanging it for a part of T; however, no safe compensation
or universal exchange theorem for this branch is yet proved.

Counts are graph-template counts, not finite valuation domains. The atlas stays
at 102 open templates overall. Code: `efr/two_singleton_escape.py`. The saved
tests check the constructive alternatives and the reachability counts. No
exhaustive continuous campaign was launched.
