# All-deletion counterexample search and a source-based repair lemma

Update: [RESTORATION_LEMMAS.md](RESTORATION_LEMMAS.md) resolves the restoration
step using the BCFF theorem with a fixed lexicographic potential, strengthens
the unique-source result to arbitrary bundle sizes, and exhibits a verified
multiple-source obstruction and an ordinary-transfer escape. The original
exploratory results below are retained as a historical record.

No counterexample to Mode C or unrestricted additive EFR existence was found.
These are exploratory local results, not a universal certificate or a GitHub
Actions run. Throughout, EFX means EFX0, including removal of zero-valued goods.

## The counterexample target

Seek one nonnegative additive 4x10 matrix V for which, for every omitted good g,
every complete EFX allocation A of the other nine goods, and every recipient k,
insertion fails. For nonempty A_k of size s, failure means that some i != k has

    (s+1) v_i(A_i) < s (v_i(A_k) + v_i(g)).

An empty target always accepts insertion. No initial partition, radius, ownership
assignment, or bundle-size profile is fixed in this experiment. A negative point
verdict requires the unrestricted exact oracle to exhaust all ten deletions and
all 11051 unlabeled partitions per deletion, including every ownership matching.

## New local experiments

`mode_c_adversary.py` searches normalized real valuations by exact QF_LRA
counterexample-guided refinement. Each successful witness adds a clause excluding
its entire feasible valuation region. Domains exclude a common least-valued good;
that is a proved positive case conditional on EFX-nine existence. Only row zero
is sorted, via one simultaneous relabeling of goods. Independent row sorting is
not used. Normalization covers nonzero valuation rows; this is not a certificate
for instances containing identically zero valuation rows.

| Domain | Successful candidate/witness checks | Final symbolic verdict |
| --- | ---: | --- |
| General normalized domain, no common least good | 164 | UNKNOWN |
| Near identical: coordinate differences from row zero at most 1/100 | 61 | UNKNOWN |
| Four common large goods >=1/8 each; remaining six <=1/32 each | 367 | UNKNOWN |

Each check has a 15-second solver cap and each domain a 120-second wall budget.
The near-identical run hit its solver cap after about 54 seconds; the others
reached the wall budget. All 592 witnesses were independently checked with the
plain exact EFX/EFR checker. UNKNOWN is neither coverage nor a counterexample.
The raw local logs store each candidate matrix and its witness. The committed
summary records the domain outcomes and final candidate matrices.

`mode_c_mutation.py` additionally performs four seeded mutation searches, with
404 candidate evaluations in total, all excluding a common least good. Each
candidate is checked exhaustively for every omitted good, minimizing first the
number of successful deletions and then the number of successful constructions.
The successful-deletion histogram is:

| Successful omitted-good choices | Candidate evaluations |
| ---: | ---: |
| 6 | 50 |
| 7 | 81 |
| 8 | 27 |
| 9 | 30 |
| 10 | 216 |

The smallest observed number is six; this is NOT a universal lower bound.
Candidate evaluations can revisit a valuation matrix and are not claimed to be
all distinct. The seeded mutation results, including four best matrices and
exhaustive per-deletion counts, are committed in `experiment-results/mode-c-adversary/`.

## A proved repair lemma without a common least-valued good

Use the strict envy graph: i -> j iff v_i(A_j) > v_i(A_i). A source means an
agent with no incoming edge, so nobody envies that agent's bundle.

**Lemma.** Suppose source k holds a singleton {h}, g is omitted, and agent i
blocks insertion of g into {h}. If i is reachable from k by a directed envy
path, there is a new EFX-nine allocation omitting h that strictly improves the
utilities of every agent on the path and leaves the others unchanged. Under
free whole-bundle matching, this move retains eight goods.

**Proof.** Since k is unenvied,

    v_i(h) <= v_i(A_i).

Blocking insertion into a singleton says

    2 v_i(A_i) < v_i(h) + v_i(g).

Together these imply v_i(g) > v_i(A_i). Take a simple path
k=a_0 -> a_1 -> ... -> a_t=i. Give a_r the former bundle A_{a_{r+1}}
for r<t, give i the singleton {g}, and omit h. Every path agent strictly
improves. The new bundle collection consists of the old bundles except that
{h} is replaced by {g}. Comparisons against the new singleton are automatic.
Comparisons against old bundles follow from original EFX and weakly higher own
utilities; if a compared old bundle was previously the observer's own bundle,
nonnegativity gives the required bound directly. Thus the allocation is EFX.
Only h and g change physical slots under the corresponding bundle matching.
QED.

The proof is a simple capacity-based specialization of the champion/rotating-
path approach, not a claim that the general champion technique is new.
`singleton_escape.py` implements the rule with exact validation.

**Corollary.** In an acyclic envy graph with a unique source holding a singleton,
either insertion into that singleton succeeds or the lemma gives a strict
Pareto improvement to another EFX-nine state. A unique source in a finite DAG
reaches every vertex, so every blocker is reachable.

**Extremal consequence.** Fix a valuation matrix and maximize the sum of own
utilities over ALL complete EFX-nine predecessors, allowing the omitted good to
vary. This is a finite nonempty set whenever a predecessor exists. A maximizer
has no strict envy cycle. If all insertions fail at this maximizer, it cannot
have a unique source holding a singleton. More generally, no singleton source
can reach any agent blocking insertion into it. Otherwise the lemma increases
the objective and contradicts maximality.

This consequence concerns an extremal state; an arbitrary starting allocation
can certainly exhibit the excluded configuration and then be repaired.

## Concrete regression with different minima

Goods are zero-indexed. The valuation rows are

    6 5 5 1 1 1 1 1 1 20
    1 3 3 3 3 3 1 1 1 20
    1 1 1 2 2 2 3 3 3 20
    1 1 1 1 1 1 2 2 2 20

Start with ({0},{1,2},{3,4,5},{6,7,8}) and omit 9. No good is universally
least-valued. This allocation is EFX, all four insertion targets fail, and the
envy graph is the path 0 -> 1 -> 2 -> 3. Applying the lemma on 0 -> 1 yields
({1,2},{9},{3,4,5},{6,7,8}), omitting 0. Own utilities rise from (6,6,6,6)
to (10,20,6,6). Inserting good 0 into agent 0's pair then yields a valid full
EFR allocation. The regression and the known large-source trap are tested in
`test_singleton_escape.py`; both tests passed.

## What still needs proving

The lemma does not guarantee that its next state has a singleton source, and
strict improvement alone does not establish that every terminal state accepts
insertion. Multiple sources and sources with larger bundles remain unresolved.

For a larger unenvied source bundle S of size s, blocked EFR insertion implies
that some subset of S+g of size s is strictly preferred by a blocker: delete
that agent's least-valued good from S+g and compare with its average value.
A minimum-cardinality subset T of S+g that is envied by any agent has no proper
one-good deletion envied by anyone. Thus T is safe to assign to its champion.
If the champion is reachable from the source, rotating an envy path and giving
T to the champion preserves EFX and improves utilities. However, it leaves
s+1-|T| goods unallocated. When |T|<s, this exits the nine-allocated-goods state
space. Controlling and redistributing this discard set is the concrete obstacle.
This explains why simply saying 'use an envy/champion cycle' is insufficient.

The next proof/search target is a potential-increasing repair for these remaining
source configurations, allowing coordinated changes and possibly temporary
multiple unallocated goods. No constant-five restriction is needed for this
broader direction. A universal progress lemma is NOT proved here.

## Literature used for direction

- Berger, Cohen, Feldman, Fiat, *Almost Full EFX Exists for Four Agents*, AAAI
  2022, https://doi.org/10.1609/aaai.v36i5.20410. Champion graphs, discard sets,
  and lexicographic progress give the relevant framework. Their almost-full
  theorem does not itself imply that the final omitted good can be inserted.
- Alkassar, Fouz, Mehlhorn, *Complete EFX Allocations Exist for Four Additive
  Agents and Up to Nine Goods*, https://arxiv.org/abs/2608.08590. This provides
  the stated nine-good existence theorem; we have not independently rerun its
  certificate corpus.

Reproduce locally from the repository directory:

    python mode_c_adversary.py --seconds 120
    python mode_c_mutation.py
    python -m unittest test_singleton_escape

Symbolic candidate counts depend on solver/runtime timing; the mutation search
uses the fixed seed 20260922 and deterministic exact comparisons.
