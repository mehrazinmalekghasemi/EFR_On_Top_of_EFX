# Trying to close one whole template: `1125_041`

Date: 2026-09-29 (Tehran). Four additive agents, ten goods, EFX0.

**Result:** the template is not closed. Four retained exact rational probes
refute successively stronger proposed repair menus. Every retained point has
an independently verified EFX Pareto escape. The experiments also identify
one missing equality reduction and a useful combined exchange lemma.

## 1. What would actually solve this template?

Fix the starting bundles

    A_0={0}, A_1={1}, A_2={2,3}, A_3={4,5,6,7,8}, g=9.

The exact strict envy graph is 2->0->1; agent 3 is isolated. Agents 2 and 3
are the two sources. A closure proof must cover **every** nonnegative additive
valuation with this graph and allocation, not merely every tested point.
It must produce either EFR insertion or an EFX move increasing the same fixed
progress potential, with restoration handled as in the project's existing
framework. Pareto improvements suffice for every physical priority.

Under the elementary reductions, D19 already handles

    z_3=v_3(g)<=u_3/2.

Thus a putative terminal state has z_3>u_3/2. The source self-pair cuts give
v_3(x)<=u_3-z_3 for all five old source items; summing them gives

    u_3/2<z_3<=4u_3/5.

Every old item of agent 3 is therefore worth less than g to that agent.
This is the high-pool region tested below. The interval is a theoretical
reduction; it does not mean half of the valuations or runtime is removed.

## 2. Ideas tested and what happened

| Idea | Exact result | Assessment |
| --- | --- | --- |
| Replace one old item in agent 3's bundle by g | A rational point defeats all five replacements | Insufficient alone |
| Allow any subset of that bundle to be retained with g | Escapes the first point, but another point defeats all 32 subsets | Useful ingredient, not a universal theorem |
| Allow weak acceptance at the end of a strict envy path | Gives a new equality-case Pareto lemma and escapes the next point | Valid reduction; does not cover strict residual cases |
| Exchange one pair-source item for any subset of agent 3's bundle, without g | Escapes the strict residual point; a further point defeats all 64 swaps | Useful but still insufficient |
| Combine an exchange, g, and releasing an old good | Escapes the last point, changing only the two source owners | Most promising new move class; universal coverage unproved |

All probes also forbid every immediate EFR insertion and every reverse-transfer
compensation meeting the earlier conservative budget. Thus the examples are
not merely failures of an arbitrarily chosen item in those menus.

## 3. How the tests were performed

For the retained points, each old own-bundle value is normalized to 100.
A bounded SMT query imposes nonnegative rational values, the exact strict envy
graph, starting EFX, pool bounds, source self-pair cuts, reachable-pair cuts,
and the specified menu failures. Additional stages forbid additional moves.
The last two stages make the reachable-pair and source self-pair bounds strict.
The normalized domain is sufficient to refute universal repair claims; it is
not asserted to cover all zero-utility boundary cases for an existence proof.

The solver returned SAT witnesses, not impossibility certificates. Their
claimed failure properties and escape allocations are checked separately by
exact rational arithmetic, enumerating only the small specified move menus.
The universal conclusions are the handwritten lemmas, not an inference from
successful examples. The helper optimization used to find escapes does not
establish any claim that the escapes are unique or globally minimal.

The four retained witnesses and allocations are in
[the evidence file](../experiment-results/template-1125-041/witnesses.json).
Reproduce a bounded candidate search with, for example:

    python scripts/research/probe_1125_041.py --stage 4

The script requires `z3-solver==5.1.0.0` and has a 20-second solver timeout.
UNKNOWN is not interpreted as success or impossibility. There is no global
valuation campaign and no inference about a multi-day completion time.

## 4. D24: a weak final champion is enough on a strict envy path

Let s=a_0->a_1->...->a_k=j be a nonempty simple strict envy path. Let T be a
bundle from the freed goods of a_0 and the pool, disjoint from the old bundles
being rotated, safe at all old utility levels. If v_j(T)>=u_j, rotate the old
bundles along the path and give T to j.

**Lemma D24.** This is an EFX Pareto improvement, even with equality at j.

**Proof.** Each earlier path agent strictly improves. The endpoint weakly
improves, other agents stay fixed, and every reassigned target remains safe
at the recipients' new utility levels. Since the path is nonempty, at least
one agent strictly improves. QED.

For T={g,h} with h in the nonsingleton source bundle, safety follows from the
pool bound and starting EFX. Consequently a terminal state must satisfy

    v_j(g)+v_j(h)<u_j

for every such reachable endpoint j and source item h, rather than merely
<=u_j. The earlier weaker inequality was valid but did not eliminate the
boundary case. Its earlier proofs are not invalidated by this strengthening.

The second retained point has v_0(g)<100 but v_0(g)+v_0(3)=100. This weak
acceptance, together with the strict edge 2->0, yields Pareto progress.
A third retained point satisfies the strict endpoint cuts and still defeats
all self-trimming and reverse-budget moves, so equality is not the whole issue.

## 5. Pool-free exchanges help, but are not enough

For h in A_2 and Y subset A_3, consider

    B_2=(A_2 minus {h}) union Y,
    B_3=(A_3 minus Y) union {h}.

There are 2*32=64 choices. The third retained point has a Pareto EFX exchange
of this type, despite failure of every reverse compensation with budget
u_3-z_3. This exposes a limitation of that budget: retaining the donor's
remainder can support an exchange that giving it only {g,h} cannot.

However, the fourth retained point defeats all 64 Pareto EFX swaps. It also
defeats the previous trimming and budget menus and satisfies strict endpoint
cuts. A proof based solely on these operations therefore cannot close the
whole template.

## 6. D25: combine exchange, the omitted good, and release

Let S=A_s,T=A_t be unenvied sources; pick h in S and disjoint Y,Z subset T.
Give

    B_s=(S minus {h}) union Y union {g},
    B_t=(T minus (Y union Z)) union {h},

leave the other agents unchanged, and release Z. The following conditions
are sufficient:

    v_s(Y)+z_s >= v_s(h),        v_t(Y union Z)<=v_t(h),   (own recovery)
    v_s(Y union Z)>=v_s(h),      v_t(Y)+z_t<=v_t(h),       (cross safety)

with at least one strict own-utility improvement, and

    R_k(B_s)<=u_k, R_k(B_t)<=u_k  for each unchanged agent k.

**Lemma D25.** These conditions imply EFX Pareto progress.

**Proof.** The first line makes both changed agents weakly better off, with
one strict gain. The unenvied-source bounds and the second line give

    v_s(B_t)<=v_s(T)<=u_s,
    v_t(B_s)<=v_t(S)<=u_t.

Thus the two changing agents do not even envy one another's entire new bundle.
Their old-target EFX checks remain valid because their own utility has not
decreased. The displayed deletion inequalities handle exactly the unchanged
observers. Disjointness is built into the construction. QED.

These are sufficient conditions, not a characterization of every combined
exchange. In this template only the two singleton owners remain to be checked.
Releasing Z is useful: it removes goods that make the donor's new bundle
unacceptable to s, while g can make up s's own loss.

For the last retained point, choose

    s=2, t=3, h=2, Y={6}, Z={7}.

The allocation becomes

    ({0}, {1}, {3,6,9}, {2,4,5,8}),

with good 7 released. Own utilities change from (100,100,100,100) to

    (100,100,21050/207,29125/207).

Every D25 inequality holds, and the allocation is independently checked EFX.
This is an escape from the tested menu obstruction, not an EFR counterexample.

## 7. A concrete path toward a whole-template proof

The current results suggest this disjunction:

1. low pool at the five-good source: use D19;
2. high pool: safe self-trimming or a weak path transfer;
3. otherwise: an exchange, possibly using g and releasing goods;
4. otherwise: a singleton blocks all such source-only changes and must enter
   the rearrangement.

Only the first branch is universally settled here. Each later move class has
proved sufficient conditions and examples where it helps. The implication
that failure of those classes forces a usable singleton-blocker move remains
unproved. In particular, we have not tested or proved universal coverage of
D25 combined with the earlier menu.

**Recommended next task:** impose failure of the D25 sufficient conditions in
the residual region and examine which singleton supplies each blocking
inequality. Try to prove those inequalities yield a safe path transfer or a
four-agent rotation. This is more promising than adding more variations of
one-good replacement, which the exact witnesses already refute as sufficient.

The case atlas stays unchanged: `1125_041` is OPEN, as are 102 templates in
all. No unrestricted EFR counterexample has been found in these experiments.
