# Three-source targets first, then return to the 31 two-singleton cases

Date: 2026-09-28 (Tehran). Nonnegative additive valuations and EFX0. Every
constructed move below is a Pareto improvement, so it preserves every fixed
physical priority. These are conditional theorems, not whole-graph closures.
The atlas remains 102 open templates (94 two-source, 8 three-source).

## 1. D21: outside the `1233_240` guard, the singleton can be the champion

Write A_o={a}, A_p=P (two goods), A_q=Q and A_r=R (three goods each).
P,Q,R are unenvied. Both q,r strictly envy a; p need not envy a.
Let u_j=v_j(A_j), z_j=v_j(g). Work under the pool and source self-pair cuts.
The reachable-pair reductions give

    z_o+v_o(x)<=u_o  for x in Q union R.

They do not necessarily give this inequality for x in P, which was one of
the missing guards in D17. Consider the branch where o blocks insertion into P:

    2(v_o(P)+z_o)>3u_o.

Since P is unenvied, z_o>u_o/2. Some h in P satisfies v_o(g+h)>u_o.
Moreover every Q or R item is worth at most u_o-z_o to o. Thus **every mixed
Q/R pair is worth less than u_o to o**.

Assume the mutual-danger configuration: r finds two Q items dangerous, and
q finds two R items dangerous, where danger means z_j+v_j(x)>u_j.

**Theorem D21.** This branch has an EFX Pareto improvement even if neither
triple owner champions an item of P.

**Proof.** As in the earlier mutual-danger proof, the source and self-pair
bounds imply every mixed Q/R pair is safe to q and r. Exchange an r-dangerous
Q item and a q-dangerous R item. Both triple owners strictly improve. The
singleton o cannot block a mixed deletion pair by the bound above. If p also
accepts the new triples, the exchange finishes the proof.

Otherwise p envies a mixed pair E={x,y}, x in Q, y in R. Choose an r-dangerous
c in Q different from x; there are two choices before excluding x. Set

    C=(R minus {y}) union {c}.

Agent r strictly improves because v_r(c)>u_r-z_r>=v_r(y). Every deletion pair
of C is safe to q by mutual danger, and to o by its mixed-pair bound. It is
safe to p as well: for a mixed pair, the source bounds give value at most

    (u_p-v_p(x))+(u_p-v_p(y))<u_p.

Unmixed deletion pairs are old source subbundles. Now give

    B_p=E, B_o={g,h}, B_q={a}, B_r=C.

All four agents strictly improve. E and {g,h} are safe pairs; {a} is a
singleton; C has just been checked against every other observer. The bundles
are disjoint. QED.

The singleton owner now receives the champion pair. This is the missing
flexibility supplied by the very violation that prevented use of D17.

The saved example has no triple-owner pair champion and gives utilities

    (300,600,300,300) -> (330,840,600,323).

**Still open in `1233_240`:** obtaining a comparable alternative when the two
triples do not have mutual two-item danger. D21 does not show that mutual
danger is forced throughout the complement of D17.

## 2. D22: a single-observer dangerous triangle can transfer to that observer

Let B=A_s be an unenvied four-good source. A pair Y subset B is forbidden for
j if z_j+v_j(Y)>u_j. Suppose one observer j supplies **all** forbidden pairs,
and j is reachable from s. The result applies in particular to a triangle
belonging to that observer, and also to a disjoint-pair obstruction.

**Theorem D22.** Under the pool bounds, there is an EFX Pareto improvement.

**Proof.** If a source self-pair {g,x} improves s, use that safe pair. Otherwise
z_s+v_s(x)<=u_s for every x in B. Choose a forbidden pair Y for j and let
T=Y union {g}; j strictly prefers T to its old bundle.

For every observer k other than s,j, absence of forbidden pairs implies
z_k+v_k(x)<=u_k for each x in B, by nonnegativity and completion of x to a pair.
The same bound holds for s by its self-pair cuts. Deleting an old item from T
therefore leaves a safe pair {g,x}; deleting g leaves an old source pair.
Thus T is safe to every agent other than its recipient j at old utility levels.
There is no need to require j's deletion values to be below its *old* utility:
j receives T and strictly improves.

Rotate old bundles along a strict envy path s->...->j and assign T to j.
All path agents improve, other agents stay fixed, and every target is safe
for the agents observing it. The allocation is disjoint and EFX. QED.

### Consequence for the four remaining (1,2,2,4) templates

If the unique observer is the singleton owner, the quad source reaches it in
`1224_208` and `1224_200`. The corresponding single-observer triangle branch
is therefore excluded as a terminal obstruction. In `1224_008` and
`1224_048`, the quad source does not reach that singleton, so this argument
does not apply. Another source can never be reached by a strict envy path
from the quad source, since it is unenvied.

The distinction "one observer has a triangle" versus "only one observer has
any forbidden pairs" matters. Extra forbidden pairs belonging to other
observers can make T unsafe; D22 does not silently discard them.

For a triangle {a,b},{a,c},{b,c} belonging to j, source unenviedness also gives

    v_j(a)+v_j(d)<z_j,
    v_j(b)+v_j(d)<z_j,
    v_j(c)+v_j(d)<z_j,

where d is the fourth source item. Summing the three original forbidden-pair
inequalities and using v_j(B)<=u_j gives

    2v_j(d)<3z_j-u_j,       z_j>u_j/3.

If j is a pair owner under its self-pair cuts, z_j<=u_j/2, so v_j(d)<u_j/4.
These bounds help describe the unreachable-observer branch but do not yet
supply its missing compensation.

## 3. Return to the 31 templates: reverse the expensive dangerous transfer

Now A_i and A_r are singletons, A_s=S is a triple, A_t=T is a four-good source,
and both singleton owners are reachable from s. Let x in S be the unique item
dangerous to t in D20:

    v_t(g)+v_t(x)>u_t.

The previous replacement failed when v_s(x)>=v_s(g). Instead give {g,x} to t.
This strictly improves t. We only need to compensate s for x.

**Theorem D23.** Suppose the source and pool bounds hold, both singleton owners
are reachable from s, and there is Y subset T such that

    v_s(Y)>=v_s(x),           v_t(Y)<=u_t-v_t(g).          (1)

Then there is an EFX Pareto improvement. No agent-priority assumption is needed.

**Proof.** Let C=(S minus {x}) union Y. The source s weakly recovers. Since S
is unenvied and x is dangerous,

    v_t(S minus {x})<v_t(g),

and hence v_t(C)<u_t by (1). First try giving C to s and {g,x} to t, leaving
the singleton owners unchanged. The new pair is safe at all old utilities.
If this allocation is EFX, it is already a Pareto improvement.

Otherwise some deletion of C is envied by a singleton owner at its old
utility. Choose a minimum-cardinality subset E of C envied by any agent at
its old utility. Every deletion of E is unenvied by every agent. Agent t
cannot champion E, since v_t(C)<u_t.

If s champions E, give E to s and {g,x} to t; both improve and all targets are
safe. If a singleton owner k champions E, use a strict path from s to k,
rotate the old singleton bundles along it, and give E to k. Independently
give {g,x} to t. The other source t cannot lie on the path. All changed agents
strictly improve, all targets are safe, and E is disjoint from {g,x}. QED.

This theorem automatically repairs singleton blockers of the proposed
compensation. It does not require guessing which singleton will object first.
It also allows several compensation goods, rather than an item-for-item swap.

### What failure now forces

There are only 16 subsets Y of T. Define the exact finite optimization

    M_s=max { v_s(Y) : Y subset T, v_t(Y)<=u_t-v_t(g) }.

Failure of this theorem requires M_s<v_s(x). This is a restriction on the
valuation region, not a finite replacement for the whole continuous search.

If h is t's dominant item and its self-pair cut holds, both {h} and T minus
{h} meet the donor budget in (1). Therefore a surviving terminal state must
satisfy both

    v_s(h)<v_s(x),        v_s(T minus {h})<v_s(x).

Also v_t(x)>u_t-v_t(g)>=v_t(h). Thus x is worth more than h to **both** source
owners, and s values x more than the entire remainder of T. These are stronger
necessary inequalities than merely saying x is too expensive to delete.
They do not yet contradict source unenviedness or prove a universal escape.

## 4. Scope, verification, and next step

| Requested target | Result | Remaining gap |
| --- | --- | --- |
| `1233_240` outside D17 | D21 handles singleton pair champion plus mutual triple danger | Other danger patterns |
| One-observer triangle at a four-good source | D22 gives progress when that observer is reachable and is the sole forbidden-pair observer | Unreachable or additional observers |
| Return to the 31 two-singleton templates | D23 reverses the dangerous transfer and resolves compensation blockers under (1) | M_s<v_s(x), and missing reachability |

The recommended next two-source target is now the residual inequality
M_s<v_s(x), rather than another arbitrary joint-split search. A universal
proof would need an alternative that changes the singleton assignment,
retains x with s, or releases a different good. That alternative is not proved
here. No whole template is removed and no exhaustive valuation workflow ran.

Code: `efr/focused_three_then_two.py`; tests:
`tests/test_focused_three_then_two.py`. Saved examples use exact integer values;
independent allocation checks and simultaneous agent relabelings verify the
implementations. The mathematical claims are supported by the proofs above.
