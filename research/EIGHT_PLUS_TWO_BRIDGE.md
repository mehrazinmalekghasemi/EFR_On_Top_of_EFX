# Eight-good EFX to ten-good EFR: proved criteria and a local obstruction

All valuations are nonnegative and additive, goods are numbered 0 through 9,
and EFX means EFX0. This note does **not** close any whole size family or graph
cell. The atlas remains at 102 open templates. It investigates the four residual
families 1125, 1134, 1224, 1233 without requiring the new predecessor to retain
its original size profile.

## B1. Exact simultaneous insertion criterion

Let C be EFX on eight goods, with omitted goods g,h. Write
u_i=v_i(C_i), k_j=|C_j|. Choose recipients p,q, allowing p=q, and let D_j be
its assigned subset of {g,h}. Put U_i=u_i+v_i(D_i).
The resulting complete allocation is EFR if and only if, for each changed
bundle j and observer i != j,

\[
(k_j+|D_j|)U_i\ \ge\ (k_j+|D_j|-1)\bigl(v_i(C_j)+v_i(D_j)\bigr).
\]

**Proof.** EFR compares own utility to the expected value of another bundle
after uniformly deleting one item: a bundle of size n has expected remainder
(n-1)v_i(B)/n. This gives precisely the displayed inequalities for changed
bundles. For unchanged bundles, EFX of C implies EFR (every deletion is bounded
by u_i), and own utilities only increase. Empty target bundles impose no
condition. These arguments prove both directions. QED.

For distinct recipients there are only six possibly new observer constraints;
for a common recipient there are three. Exactly 16 ordered recipient choices
cover all ways to distribute the two goods. In particular an observer receiving
h may tolerate insertion of g when it could not do so before receiving h.

## B2. Simultaneous insertion can succeed when every first insertion fails

Give each agent a pair of unit-valued old goods, eight goods in total. All
agents value every old good at 1. Agents 0 and 1 each value both g,h at 2;
agents 2 and 3 value both at 0. The eight-good allocation is EFX.

Inserting either new good into any one bundle fails EFR: at least one of agents
0,1 remains at utility 2 and sees an enlarged triple of value 4, with expected
remainder 8/3 > 2. Nevertheless giving g to 0 and h to 1 yields EFX, hence EFR:
own utilities are 4,4,2,2; for agents 2,3 every deletion from an enlarged triple
leaves value at most 2. The remaining comparisons are immediate unit-pair or
value-at-most-4 comparisons.

Thus an eight-good bridge should test the two insertions **jointly**, without
requiring the intermediate nine-good state to be EFR or EFX. This statement is
about one fixed predecessor, not failure of all nine-good predecessors.

## B3. Exact condition for deleting one good from EFX-nine

Let A be EFX on nine goods, h in A_t, and define
R_i(B)=max_{x in B} v_i(B minus {x}), with R_i(empty)=0.
Deleting h preserves EFX exactly when

\[
v_t(h)\le v_t(A_t)-\max_{j\ne t}R_t(A_j).
\]

**Proof.** Only t loses own utility. Its comparisons against the three
unchanged bundles are exactly this bound. All other agents keep their utility;
a deletion from the shortened target A_t minus {h} has value at most the
corresponding deletion from A_t, by nonnegativity. QED.

This exposes two separate obstructions: no removable good at all, or every
removable good fails the B1 insertion tests. Both occur in the retained data.

## B4. The omitted pair cannot be fixed arbitrarily

Take identical valuations: eight goods of value 1 and two goods g,h of value
100. If g,h are omitted, every EFX-eight allocation must have two unit goods
per agent. Indeed EFX implies bundle sizes differ by at most one; four such
sizes totaling eight must all equal two. There are 8!/(2!)^4 = 2520 labeled
allocations of this form.

After assigning g,h, at least two agents still have utility 2. A bundle with
one large good has expected remainder (2/3)*102=68; if both go to the same
bundle it has expected remainder (3/4)*202. EFR fails in either case.

Changing the omitted pair solves this instance: omit two unit goods; allocate
the two 100-valued goods as singleton bundles and split the six remaining unit
goods 3+3. This is EFX. Add a unit good to each small-good owner; the resulting
allocation is again EFX. Thus failure for one pair cannot reject the route.

## Attempt to solve 1125: encouraging examples, then a rigorous obstruction

Start with singleton owners a,b, pair owner p, and five-good owner d. Consider
removing h from d and giving g,h to two distinct owners among {a,b,p}.
There are five choices of h and six ordered recipient choices: **30 candidates**.
B3 and B1 certify any success. This is a sufficient menu, not a universal lemma.
It resolves all five previously saved 1125 witnesses, including all four
progressively strengthened `1125_041` probes.

We then explicitly searched for failure of the stronger menu: remove **any**
of the nine old goods, require the resulting eight-good allocation to be EFX,
and allow **all 16** recipient pairs. The exact rational solver found SAT in
about 0.17 seconds in normalized template `1125_041`. The saved matrix has
A=({0},{1},{2,3},{4,5,6,7,8}), omitted good 9, and precisely envy edges
0 -> 1 and 2 -> 0. Sources are 2,3; every own utility is 100.

The only EFX-preserving deletions are h=4,5,6,7. All 64 extensions of those
four predecessors fail EFR, as do all four direct insertions of good 9.
An independent Fraction-based test checks the graph, EFX, all these failures,
and the successful escape below. This is a finite, exact counterexample to
this local strategy, **not** a counterexample to EFR existence or global 8+2.
The probe does not impose every earlier repair-menu exclusion, so it is not
claimed to defeat their union.

Allow rebundling and omit {0,1} instead. The following eight-good predecessor
is EFX, and giving good 0 to agent 2 and good 1 to agent 0 yields EFR:

| Agent | EFX-eight bundle | Final EFR-ten bundle |
| --- | --- | --- |
| 0 | {2} | {1,2} |
| 1 | {4,5,6,8} | {4,5,6,8} |
| 2 | {9} | {0,9} |
| 3 | {3,7} | {3,7} |

Exact values and witness: [no-local-1125.json](../experiment-results/eight-plus-two/no-local-1125.json).
This illustrates a successful escape; it proves neither that changing the pair
is necessary for this instance nor that this escape form always exists.

## Results across the four families

The following counts concern the fifteen **previously retained** instances.
The newly generated 1125 obstruction is additional.

| Initial family | Retained instances | Local drop-one bridge succeeds | Free rebundling and pair choice succeeds | Universal status |
| --- | ---: | ---: | ---: | --- |
| 1125 | 5 | 5 | 5 | OPEN; new local-strategy counterexample |
| 1134 | 1 | 0 | 1 | OPEN |
| 1224 | 1 | 1 | 1 | OPEN |
| 1233 | 8 | 0 | 8 | OPEN |

The new 1125 obstruction also has a free bridge: **16/16 instances have a
verified eight-good bridge**. Sample success is not a quantified existence
proof. Of the eight 1233 instances, five admit no EFX-preserving deletion at
all; the other three permit deletions but no successful local extension.

## What should be proved or searched next?

1. **Keep 1125 as the first theoretical target, but allow a changed omitted
   pair and exchanges involving singleton owners.** A useful missing lemma
   is: failure of the local bridge inequalities forces either a previously
   proved safe progress move or an eight-good bridge after rebundling. The new
   obstruction is a mandatory regression example for any proposed move menu.
2. **Separate terminal bridges from progress moves.** A verified EFR-ten
   bridge terminates the construction and needs no potential increase. A
   nonterminal EFX-nine repair still must increase the one fixed potential
   already used by the project. Arbitrary rebundling is not automatically a
   valid progress step; agent priority must remain tracked.
3. **Use exact per-instance exhaustion as a counterexample filter.** For one
   valuation matrix, all 45 omitted pairs and all 4^8 labeled assignments
   give at most 2,949,120 predecessor candidates. Each EFX candidate has 16
   recipient choices. This includes empty bundles, zeros, ties, and all agent
   labels. No independent row sorting is used. Code stops early on a verified
   witness; only completed negative scans yield NO_BRIDGE, limited to the
   declared pair scope. Deadlines yield UNKNOWN. `pairs_scanned` counts pairs
   considered, including the pair of an early witness, not fully exhausted pairs.
4. **For the other families, use bounded adversarial searches to discover
   missing moves, then certify valuation regions.** Finite allocation
   exhaustion for a fixed matrix does not exhaust the continuous valuation
   domain. A universal proof requires coverage of all matrices, for example
   exact linear-region certificates for failure of a proved sufficient menu.
   A SAT matrix is a menu obstruction until the broader oracle is run; UNSAT
   is useful only with checked assumptions and an auditable certificate.

Positive fixed-instance bridge searches here took under one second apiece.
These are early-success times, not worst-case negative exhaustion benchmarks
or estimates for universal closure. No multi-day workflow was launched: these
measurements do not justify a three-to-four-day universal search claim.

## Reproduction

- `python -m scripts.research.probe_eight_plus_two`
- `python -m scripts.research.probe_no_local_eight_bridge` (requires z3-solver;
  bounded 20-second SAT probe, model may vary)
- `python -m unittest tests.test_eight_plus_two -v`

The oracle uses row-scaled exact integers, with Python big integers when its
conservative int64 bound is exceeded. Witness tests use independent rational
arithmetic and literal deletion comparisons. Evidence is retained in
[results.json](../experiment-results/eight-plus-two/results.json).
