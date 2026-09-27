# Three sources, compensation, and a fixed progress potential

Follow-up: [DANGEROUS_ITEM_PROGRESS.md](DANGEROUS_ITEM_PROGRESS.md) now proves
the entire both-champion branch (D4) and adds a residual compensation theorem
(R1). The whole-graph atlas remains unchanged.

Date: 2026-09-27. Scope: four agents, ten goods, nonnegative additive values,
EFX0. This note adds human proofs of conditional progress statements. **It does
not close a whole case in the 103-case atlas**, prove universal three-agent
repair, or establish Mode C. No exhaustive valuation search was used.

## 1. Fixed framework and notation

Fix physical agent identities and a priority order pi once for the entire
argument. Set

    Phi_pi(A) = (v_pi[0](A_pi[0]), ..., v_pi[3](A_pi[3])).

Every nonterminal step must strictly increase this same lexicographic tuple.
Restoration uses that same pi, through the theorem already documented in
[RESTORATION_LEMMAS.md](../RESTORATION_LEMMAS.md). Terminal complete EFR need not
improve the tuple. Nothing below chooses a new priority after seeing a move.

Write u_i=v_i(A_i), z_i=v_i(g), and

    R_i(S) = max_{h in S} v_i(S minus {h}),     R_i(empty)=0.

Call S **safe at A** when R_i(S)<=u_i for every i. All old bundles are safe at A,
including for their original owner. Under the pool bound z_i<=u_i, a pair
containing g and an item from an old nonsingleton bundle is safe. A pair of old
items from nonsingleton bundles is also safe. These follow from EFX0 and
nonnegativity, including zeros and ties.

For a hypothetical terminal extremal state, we may use the already proved
necessary conditions:

- the envy graph is acyclic;
- z_i<=u_i;
- no safe champion closes an envy path;
- in particular z_i+v_i(h)<=u_i for h in A_i when |A_i|>=2;
- the pair-compensation move of T8 is unavailable.

A violation supplies progress immediately. These are **necessary extremal
conditions**, not assumptions satisfied by every arbitrary EFX predecessor.

## 2. Three-source structure

### S1. Star structure and champion restrictions

In each of the nine open three-source templates, A_0={a}, agents 1,2,3 are
sources, and every envy edge is s->0. Their sizes are (1,2,2,4) or (1,2,3,3).
Let E={s: v_s(a)>u_s}, a nonempty subset of the sources.

This structure follows from the graph itself: a source cannot receive an edge;
with three sources the only possible target is the fourth vertex. The atlas
already excludes the other size profiles. Consequently

    v_i(A_s)<=u_i       for every source s and every agent i.

If insertion at source s is blocked, the minimum-cardinality envied-subset
argument supplies a safe T subset of A_s union {g}, with g in T and
|T|<=|A_s|. A champion of T cannot be s, or agent 0 if s belongs to E:
otherwise an envy-path rotation gives progress. Thus the remaining champion
must be another source, or agent 0 when s is not in E.

**Proof.** The source is unenvied, so no subset of A_s is envied. Failed EFR
insertion implies an envied subset of size at most |A_s| by average deletion.
Choose a globally minimum-cardinality envied subset; every one-good deletion
is unenvied. The reachability exclusion is the existing safe-champion lemma.

**Useful consequence.** In `1233_248`, all three sources envy the singleton.
Choose one safe champion for each blocked source. Each champion is a different
source, so the resulting directed graph on the three sources has a 2- or
3-cycle. This is a rigorous structural reduction, **not an allocation move**:
all three proposed champion bundles contain the same g. Allocating the bundles
around that cycle would allocate g more than once. A proof must resolve this
competition for g.

A relay in which agent 0 receives a champion bundle from a source can only
help a terminal star when that donor is outside E. In particular that relay
cannot, by itself, settle the all-envious-source case `1233_248`.

### S2. High-pool triples and the exact replacement obstruction

Let t own a triple Q and suppose

    z_t > u_t/2,       z_t+v_t(y)<=u_t for every y in Q.

Then replacing any y_0 in Q by g strictly improves t: every old item is worth
at most u_t-z_t<z_t. Define the set of dangerous old items

    D_t = union over j != t of {y in Q: z_j+v_j(y)>u_j}.

The replacement is EFX **if and only if** D_t is contained in {y_0}.
In particular |D_t|<=1 guarantees a Pareto-improving EFX replacement.

**Proof.** The new triple's one-good deletions are its old two-good subset,
which is EFX-safe, and pairs {g,y} for the two retained items. Those pairs are
acceptable to observer j exactly when y is not dangerous for j. All other
bundles and observers' own utilities are unchanged; t's utility increases.

If Q is a source and observer j has z_j<=u_j/2, at most one item of Q is
dangerous for j. Two dangerous items would have combined value greater than
2(u_j-z_j)>=u_j, contradicting v_j(Q)<=u_j. Conversely, two dangerous items
force z_j>u_j/2. If j also owns a triple and has no self-pair improvement, then

    u_j/2 < z_j <= 2u_j/3.

The upper bound follows by summing v_j(h)<=u_j-z_j over its three own items.
Moreover, Q cannot contain three dangerous items for this observer: their
sum would exceed 3(u_j-z_j)>=u_j.

This replaces a vague “a triple replacement might fail” with a precise
obstruction: the union of dangerous items has size at least two. Separate
observers may contribute different items; counting at most one per observer
alone is insufficient.

### S3. A proved subcase of the all-envious-source configuration

Consider `1233_248`. Write p for the pair owner and q,r for the triple owners.
Assume the necessary extremal conditions in Section 1 and blocked insertion.
Suppose **exactly one** triple owner, q, champions a pair {g,h} from A_p:

    z_q+v_q(h)>u_q for some h in A_p,
    z_r+v_r(x)<=u_r for every x in A_p.

If q precedes r in the fixed priority, this state admits an EFX improvement.
Therefore this valuation-and-priority subregion cannot be extremal.

**Proof.** Agent 0 cannot block insertion at A_p: a blocking inequality would
produce a safe pair champion reachable along p->0. Hence one of q,r blocks.
By the second displayed condition r cannot block, so q blocks. Since A_p is
unenvied,

    2(v_q(A_p)+z_q)>3u_q  implies  z_q>u_q/2.

Choose h in A_p championed by q. Failure of pair compensation implies
v_p(y)<v_p(h) for all y in A_q. The self-pair bound at p gives
z_p+v_p(h)<=u_p. Thus no item of A_q is dangerous for p.
No item of A_q is dangerous for 0 either, by safe-pair reachability q->0.

Apply S2 to q. If r finds at most one item of A_q dangerous, delete that item
(or any item if none) and replace it by g. This is Pareto progress.
Otherwise choose two dangerous items y_1,y_2 in A_q. S2 gives

    u_r/2 < z_r <= 2u_r/3,
    v_r({y_1,y_2}) > 2(u_r-z_r) >= z_r.                 (1)

If q finds no item of A_r dangerous, replace one item of A_r by g:
agent 0 finds no dangerous item by r->0; p finds at most one because it owns
a pair, z_p<=u_p/2, and A_r is a source. Delete that possible item. Agent r
strictly improves and the result is EFX by S2.

Otherwise choose x in A_r with z_q+v_q(x)>u_q. Give

    B_q={g,x},       B_r={y_1,y_2},

and leave agents 0,p unchanged. Both new bundles are safe pairs at the old
utility levels. Agent q improves. Agent r may lose, but its new value exceeds
z_r by (1). Its EFX comparisons require only the following bounds:

- against B_q: v_r(g)=z_r and v_r(x)<=u_r-z_r<z_r;
- against A_p: each item is <=u_r-z_r<z_r, by r's nonchampionship assumption;
- against A_0: deletion leaves the empty set.

So B is EFX. The only possible loser is r, and q precedes r, giving strict
progress in the fixed Phi_pi. Released goods are handled by fixed-potential
restoration. QED.

This proof actually uses at most two changing agents in its final branch.
It does not contradict the known two-agent obstruction, which is in a
different configuration. The both-champion branch is now settled by D4 in the follow-up note.
A sole champion that follows the other triple in priority remains unresolved. We do not relabel q to make it earlier.

## 3. A stronger three-agent compensation theorem

### C1. Safe relay with optimal two-good compensation

Choose distinct agents s,i,t; let r be the fourth. Suppose |A_s|,|A_t|>=2,
and choose a bundle T satisfying

    g in T subset of A_t union {g},
    R_j(T)<=u_j for every j,
    v_i(T)>u_i,           v_s(A_i)>=u_s.

Let

    H = A_s union (A_t minus T),
    L_t = max(R_t(T), R_t(A_i), R_t(A_r)).

Choose C to be the two goods of H most valued by t. There are at least two
goods in H since A_s is a nonsingleton. Set

    B_s=A_i,       B_i=T,       B_t=C,       B_r=A_r.

Let G contain i and also s if v_s(A_i)>u_s. Define the required compensation

    K_t = L_t                 if some member of G precedes t,
          max(L_t,u_t)        otherwise.

**Theorem.** If v_t(C)>=K_t, then B is EFX and Phi_pi(B)>Phi_pi(A).
Moreover, this inequality is necessary and sufficient for *some compensation
bundle of at most two goods from H* to make this particular relay EFX and
strictly improve Phi_pi. Thus choosing the top two is an exact solution to
this compensation subproblem, not a heuristic.

**Proof.** H consists of items from old nonsingleton bundles, hence every
item of H is worth at most u_j to every observer j. Consequently C is safe at
all old utility levels. The other new target T is safe by assumption, and
A_i,A_r are old safe targets. Agents s and i weakly improve, i strictly, and
r is unchanged. Their EFX inequalities therefore hold. The donor t's exact
remaining EFX requirement is v_t(C)>=L_t.

Only t can lose. If a strict gainer precedes t, such a loss is allowed by the
fixed lexicographic tuple. Otherwise t must weakly retain u_t; a strict gain
by t or the later strict gain by i then makes the tuple increase. These are
exactly the two definitions of K_t. Nonnegativity means the top two maximize
t's compensation value among all subsets of H of size at most two. All such
subsets are safe for the other agents, so no further constraint distinguishes
them. Disjointness follows from the definition of H. QED.

**How this strengthens T10.** T10 returns the entire old A_s to the donor.
C1 may also use the donor's retained items, and can discard goods to keep the
new target a safe pair. Neither lemma subsumes the other: sometimes a large
A_s is needed to compensate enough, while sometimes mixing retained and
released items works better. Both keep the same priority.

The safe-pair specialization T={g,h}, h in A_t, needs no separate safety
verification once the pool bound holds. At most 24*10 ordered proposals are
needed for a fixed point. This is a small sufficient-move diagnostic, not
exhaustive valuation-space coverage.

### Explicit witness on the verified two-agent obstruction

Use the saved base matrix in [TWO_SOURCE_PROGRESS.md](../TWO_SOURCE_PROGRESS.md),
with (s,i,t)=(2,0,3), g=9, T={5,9}, and priority (0,1,2,3).
The top two compensation goods are 4 and 3. The resulting allocation is

    B=({5,9},{1},{0},{3,4}),
    own utilities: (108,6461,902,694) -> (109,6461,1821,692).

Here L_3=363 and compensation has value 692. EFX holds despite the donor's
loss. The same proposal fails the lexicographic test under priority (3,2,1,0):
the required value then becomes 694. This demonstrates why priority is part
of the state. This witness releases four goods; restoration is a theorem
dependency, not implemented by the local relay code.

### What is still missing for the 94 two-source cases

C1 guarantees a valid move **when its explicit inequalities hold**. It does
not guarantee that suitable s,i,t,T exist in every two-source template.
In particular it requires s to weakly prefer A_i and enough two-good value
in H. Larger compensation bundles may be needed, in which case their EFX
safety must be proved separately. A minimal safe champion T can replace the
pair specialization, but its existence does not imply compensation.

The next real theorem would be a disjunction: every extremal candidate has
an EFR completion, an existing progress move, a C1 relay, or a specified
broader safe compensation move. Merely renaming C1 a universal lemma would
leave its principal existence obligation unproved.

## 4. Priority-aware symmetry: exact counts, not a guess

### P1. Decorate the graph before using lexicographic cuts

An agent relabeling p must carry all of the following together: valuation
rows, bundle ownership, graph vertices, and priority

    (pi[0],...,pi[3]) -> (p(pi[0]),...,p(pi[3])).

The resulting tuple has the same numerical coordinates and ordering, so
lexicographic comparison is invariant. Relabeling the bundles and rows while
resetting priority to (0,1,2,3) does not have this property.

For a fixed canonical size profile and graph, let Aut be its size-preserving
graph automorphism group. Its action on the 24 total priority orders is free:
if p fixes the entire ordered tuple it fixes all four agents, hence is the
identity. Thus the exact number of priority representatives is 24/|Aut|.

The standard-library generator `python -m efr.priority` gives:

| Region family | Undecorated graph templates | Priority-decorated templates |
| --- | ---: | ---: |
| Two sources | 94 | 2,136 |
| Three sources | 9 | 156 |
| Total | 103 | 2,292 |

| Three-source ID | Priority representatives |
| --- | ---: |
| 1224_008 | 24 |
| 1224_048 | 12 |
| 1224_208 | 24 |
| 1224_200 | 12 |
| 1233_008 | 12 |
| 1233_048 | 24 |
| 1233_248 | 12 |
| 1233_040 | 24 |
| 1233_240 | 12 |

These are not 2,292 newly discovered counterexample regions and not a runtime
estimate. They are the required bookkeeping if a symmetry-reduced argument
uses an arbitrary fixed physical priority. The original 103-template count
remains correct for priority-independent Pareto cuts. All priority orbits and
representatives are saved in [priority-cases.json](priority-cases.json).

## 5. Recommended next proof tasks

1. In the nine stars, split by singleton enviers E and champion destinations.
   Use S1 to avoid trying singleton-champion relays where reachability already
   rules them out. Retain the source profiles; their capacities differ.
2. Extend S3 to its two missing branches, especially simultaneous champions of
   the pair. Track dangerous items using S2. A cardinality or additive-sum
   contradiction would be preferable to enumerating whole allocations.
3. For each two-source topology, seek a path s->i and a source donor t on the
   other component. Use C1 to reduce compensation to the scalar comparison
   v_t(top-two(H))>=K_t. If it fails, use that strict deficit as a new necessary
   inequality; do not assume it fails for every possible relay.
4. Attempt to prove that all such deficits force a different safe move or an
   EFR insertion. Allow a larger safe compensation bundle when the top-two
   class is too restrictive. Keep the same Phi_pi throughout.
5. Only after these mathematical splits should a solver encode the remaining
   regions, with explicit priority representatives. A time budget still does
   not establish exhaustive completion, and no multi-day workflow is launched.

## Reproduction and implementation scope

From the repository root:

    python -m unittest discover -v
    python -m efr.case_status --check
    python -m efr.priority --out research/priority-cases.json

`efr/compensation.py` implements C1 for a supplied safe T and the bounded
pair-proposal generator. Tests independently check the witness's fairness,
reject the donor-first priority, check all 24 simultaneous relabelings, and
check that all priority orbits cover the 24 orders exactly once. S1–S3 are
human arguments above; no solver result is substituted for their proofs.

Validation after the folder move: all 53 tests pass; the case atlas regenerates
exactly; the independent base and nondegenerate 8,532-assignment checks still
confirm the existing two-agent obstruction and its positive escape witnesses.
The retained continuous-region SMT certificates were not changed or re-solved.
