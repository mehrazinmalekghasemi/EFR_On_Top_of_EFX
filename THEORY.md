# Exact EFX9 → EFR10 search for four additive agents

For the current research classification, see [RESEARCH_STATUS.md](RESEARCH_STATUS.md) and [CASE_ATLAS.md](CASE_ATLAS.md). This note documents the original oracle and full-domain search architecture.

This package implements the proposed delete-a-good / find-EFX / compute-capacities / insert procedure, and a resumable symbolic search over the entire normalized valuation domain. It includes a fast exact point oracle, process parallelism, an independent region-cover verifier, benchmark results, and counterexamples to two overly strong variants of the approach.

**A one-week run is supported. A completed whole-space proof within one week is not guaranteed.** No global existence result is claimed by this delivery. The supplied short region-search pilot did not close the domain. A timeout, an unfinished branch, or a failed restricted heuristic is never counted as a theorem.

## Install and run

Tested on Linux x86-64, Python 3.12, NumPy 2.3.5, Numba 0.67.0, Z3 5.1.0. The Python entry points use multiprocessing spawn and are portable to macOS; Apple Silicon has not been benchmarked here. Numba compiles the exact integer oracle on its first call and caches it. Compilation/startup is excluded from warm kernel timings but recorded separately by the benchmark.

```bash
unzip efr_github_ready.zip
cd efr-github
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m unittest -v test_engine
```

For a particular ten-good instance, supply four JSON rows of ten nonnegative numbers. Integers, exact decimals, and rational strings such as `"3/7"` are accepted. Agents and goods are numbered from zero. Rows need not already be normalized.

```bash
python3 oracle.py examples/sample.json --out allocation.json
```

The result includes the deleted good, the complete EFX predecessor, recipient, final EFR allocation, and exact scaled capacity margins. Bundles are bitmasks: mask 13 denotes goods {0,2,3}. To list goods in a bundle, use `[g for g in range(10) if mask & (1 << g)]`.

For complete EFX and insertion counts for all deleted goods:

```bash
python3 oracle.py examples/sample.json --all --out full-profile.json
```

This stores a bounded number of witnesses while counting all successful labeled predecessors/recipients. `complete: true` is required to interpret counts as exhaustive. Every negative `ABSENT` verdict is exhaustive within the declared restrictions. Deadline interruption is `UNKNOWN`.

For a nine-good matrix alone, obtain an EFX0 allocation with:

```bash
python3 oracle.py matrix9.json --goal efx9 --out efx9.json
```

Calibrate the point oracle and run a one-hour symbolic pilot on your machine:

```bash
python3 benchmark.py --count 100 --workers 1 --out benchmark-serial.json
python3 benchmark.py --count 1000 --workers 8 --out benchmark-parallel.json
python3 search.py --goal extension --workers 32 --hours 1 --out pilot
```

The parallel benchmark includes worker launch costs; small workloads may therefore be slower. It measures independent valuation profiles, not proof throughput.

A six-day search with one day reserved for independent replay:

```bash
python3 search.py --goal extension --workers 32 --hours 144 --out week-run
python3 verify.py week-run --workers 32 --hours 24 --timeout 120
```

`--hours` is a cooperative wall-time budget; formula construction and process shutdown can add overhead. For a strict outer one-week limit on Linux with GNU coreutils:

```bash
./run_week.sh 32 week-run
```

The wrapper uses GNU `timeout` with a ten-second kill grace inside a 604800-second envelope. It can stop with `INCOMPLETE_NO_THEOREM`; enforcing the deadline does not force the mathematics to finish. Exit code 124 means the outer timeout fired. Verifier exit code 2 means no verified complete cover. Atomic checkpoints preserve the most recently completed witness batch.

Repeat the same search command and output directory to resume. An existing directory cannot be reused for a different goal. Do not run two coordinators against one output directory. Each process uses one solver thread; choose workers to fit both available cores and measured RAM. More workers cannot accelerate a single hard region without splitting it.

## Exactly what is searched

There are three distinct goals:

| `--goal` | Statement whose regions are being covered |
|---|---|
| `extension` (default) | For every instance, **some** good g, **some** EFX0 allocation of the other nine goods, and **some** recipient yield EFR by insertion. |
| `efr` | For every ten-good instance, some EFR allocation exists. The search tries Mode C first, then a complete direct EFR oracle if necessary. The stored region witnesses only certify final EFR, not an EFX predecessor throughout the region. |
| `efx9` | Every nine-good instance has a complete EFX0 allocation. This reproduces the type of existence question already settled by Alkassar–Fouz–Mehlhorn; it is not their certificate corpus or an implementation of all their reductions. |

For `extension`, failure of all insertion choices refutes **this construction**, not necessarily EFR existence. The output separately attempts direct EFR at that exact valuation. If that diagnostic times out, the diagnostic remains unknown.

### Why a nine-good polytope alone is insufficient

The normalized base domain is

    P9 = {a >= 0 : sum(h=0..8) a[i,h] = 1 for every i},

which has dimension 4(9-1)=32. An unspecified tenth good adds four parameters t[i]. On rows with positive base total, the extension domain can be represented as P9 × R_{≥0}^4. The case where an agent values only the added good also needs boundary treatment in that parameterization.

The implementation instead uses the compact, complete normalization

    P10 = {v >= 0 : sum(h=0..9) v[i,h] = 1 for every i},

of dimension 36. This includes residual-zero rows without special strata. Equivalently, use nine nonnegative coordinates per agent with sum <=1 and let the tenth be the residual. Those nine coordinates do **not** themselves sum to one.

Positive independent row scaling preserves EFX, EFR, and insertion feasibility. Completely zero rows are included by the usual replacement argument: replace such a row by any positive normalized row, find a witness, then revert it. The reverted agent's inequalities are all trivial and other agents' inequalities do not depend on that row.

Only agent 0's goods are sorted, using one common permutation of goods for every row. Agents 1–3 are permuted to put their chosen favorite-good indices in nondecreasing order. This yields 220 roots for ten goods or 165 for nine goods. Ties are included by non-strict inequalities. Sorting each row's goods independently would change the instance and is not done.

P9 contains uncountably many points. An exhaustive search means proving coverage by finitely many allocation-validity regions, not enumerating points. Even checking all original simplex vertices is insufficient: different allocations may cover different vertices while leaving an interior gap. For example, [0,0.4] union [0.6,1] covers both vertices of [0,1] but not its interior.

A denominator-Q grid has binomial(Q+8,8)^4 profiles for nine goods, before symmetry reduction:

| Q | Profiles |
|---:|---:|
| 2 | 4,100,625 |
| 5 | 2,743,558,264,161 |
| 10 | 3,666,315,676,495,854,096 |

Even the complete grid only proves a statement about that finite grid, not all real valuations.

## Capacity lemma and the exact oracle

For an EFX0 predecessor A on nine goods, let s=|A[k]| and insert g into A[k]. Additivity gives

    EFR(i,j) iff |A[j]| v_i(A[i]) >= (|A[j]|-1) v_i(A[j]).

All EFR inequalities survive automatically except those in which another agent i compares with the enlarged bundle of k. Their necessary and sufficient conditions are

    (s+1) v_i(A[i]) >= s (v_i(A[k]) + v_i(g)),   for all i != k.

For s>0 the capacity is

    C[i,k](A) = ((s+1)/s) v_i(A[i]) - v_i(A[k]),

and insertion works exactly when v_i(g) <= C[i,k](A) for all i != k. Capacities may be negative. If s=0, insertion is always safe: the target becomes a singleton. The recipient's own utility only increases. We evaluate the multiplied integer form, never rounded divisions.

### Sharing work across agent assignments: a matching characterization

Enumerate an **unlabeled** partition B=(B0,B1,B2,B3) of nine goods, including padded empty blocks. Define, for each agent i,

    T_i = max_b [v_i(B_b) - min_{h in B_b} v_i(h)],

with the empty term equal to zero. Agent i may receive block c in an EFX allocation exactly when

    v_i(B_c) >= T_i.

Including the agent's eventual own block in the maximum does not strengthen the condition, because its value is at least its value after a removal. Thus **EFX assignments of a fixed partition are exactly the perfect matchings** of this four-by-four agent–block graph.

To test insertion into block b, remove an edge i→c with c!=b whenever

    (|B_b|+1) v_i(B_c) < |B_b| (v_i(B_b)+v_i(g)).

Keep the edge i→b: that agent would be the recipient. The filtered graph has a perfect matching **if and only if** this partition admits an EFX predecessor and a feasible insertion into b. This avoids guessing the recipient's identity in advance.

There are only

    sum(k=1..4) S(9,k) = 11,051

unlabeled partitions, versus 4^9=262,144 labeled allocations. All 65,536 possible four-by-four graphs are pretabulated, including all compatible permutations. Across ten deletions this is 110,510 partition visits versus 2,621,440 labeled allocations; up to four target-block graph tests are made per surviving partition. The roughly 23.7-fold reduction in partitions is a guaranteed combinatorial reduction, **not a universal 23.7-fold wall-time speedup**. Matching and table-building also cost time.

Hall's theorem supplies a useful theoretical description of an obstruction: a failed target graph has a nonempty set of agents whose acceptable blocks number fewer than those agents. Only 15 agent subsets are possible. Proving that some partition and target avoid these deficiencies is an exact reformulation of the extension question, not yet a proof of it.

Implementation details that affect correctness/performance:

- Precompute every agent's subset sum and subset minimum once per profile.
- Use a compiled Numba integer kernel, not threads contending for Python's GIL.
- Convert rational rows to primitive integer rows by exact LCM/GCD scaling.
- Use int64 only if 32 times every row sum fits; all arithmetic then has a conservative overflow bound. Otherwise use exact Python arbitrary-precision integers, which can be substantially slower.
- Try balanced partitions and small added goods first, but remove no case from unrestricted search.
- Account for repeated empty blocks when counting labeled allocations.
- Independently verify every returned witness using the original fairness definitions.
- Preserve agent ownership. Unlabeled partition enumeration is safe because ownership is recovered by matching; sorting the final labeled bundles is not safe.

For a fixed point, finding an allocation is discrete. A plain LP relaxation permits fractional goods and does not solve this problem. For a **fixed candidate allocation**, fairness constraints are linear; the universal region search needs Boolean combinations of these constraints, hence exact QF_LRA solving.

## Region search, proof scope, and replay

At a region R and finite witness menu W, the search asks

    exists v in R such that every witness in W is invalid at v?

A witness for `extension` encodes BOTH the predecessor's EFX inequalities and the three capacity inequalities. For `efr` it encodes final EFR only. Therefore an EFR-cover certificate is not accidentally presented as an extension theorem.

- SAT: extract the solver's exact rational valuation, run the complete point oracle, and add valid labeled witnesses.
- UNSAT: the menu covers the whole region, including irrational points and equality boundaries.
- UNKNOWN: retain an open region. No coverage conclusion.
- Exhaustive oracle failure: retain the exact valuation and distinguish the failed theorem from the direct-EFR diagnostic.

The solver is incremental within a task. It never rebuilds all prior constraints between individual witness batches. Every batch is checkpointed. After the configured number of visits (default two), the coordinator may pin the next favorite of one agent and enqueue **all** possible remaining choices. Non-strict order constraints ensure the children cover the parent, including ties. Child tasks inherit the parent's witnesses and run independently. `--no-split` instead keeps refining a root's finite witness menu; the unlimited idealized CEGAR procedure has only finitely many possible witnesses, but that finite bound is too large to imply practicality.

Initial budgets are 60 seconds per region task and 10 seconds per SMT call; repeat visits double both budgets up to 4x. Splitting starts after two visits by default. There are 64 refinement rounds and 8 point witnesses per round. They are configurable heuristics, not proven optimal values. Full rankings still may be hard: at maximum rank depth an open node is requeued with bounded larger budgets. Splitting is sound and creates parallel work, but is not guaranteed to reduce total CPU time.

`verify.py` imports neither the search code nor the point oracle. It:

1. Enumerates all required roots itself.
2. Validates each region's prefixes, parent, split choice, and entire child set.
3. Validates all allocation masks and their agent ownership.
4. Rebuilds full fairness formulas. For extension witnesses it uses EFX plus **all final EFR inequalities**, independently of the capacity encoding.
5. Solves each covered leaf again from scratch, with no search solver state.
6. Accepts only if every required root is covered and every required leaf is independently UNSAT.

Only `VERIFIED_GLOBAL_COVER` is a completed whole-domain result. `SEARCH_COVERED_REQUIRES_VERIFY_PY`, a covered leaf, a shard result, or `INCOMPLETE_NO_THEOREM` is not that result. Replay SMT files are included for covered leaves. These are UNSAT instances, **not formally checked proof objects**; Z3 and the verifier remain in the trust base. Do not invoke verification with Python's `-O` flag.

For several machines, use distinct output directories and deterministic root shards:

```bash
python3 search.py --goal extension --workers 32 --shards 4 --shard 0 --hours 144 --out machine0
python3 verify.py machine0 --shards 4 --shard 0 --workers 32 --hours 24
```

Run shards 1, 2, and 3 on the other machines. A shard verdict proves only its named subset. The standalone engine does not merge trees automatically. In this GitHub edition, ci.py aggregates fresh independent shard-verification reports only when every shard is present, all expected root counts match, and the code fingerprint and goal agree. A standalone global replay instead needs a collected tree containing all roots and their descendants, with the same config. Do not overwrite completed root trees with another shard's unused placeholder roots.

## Two rigorous counterexamples relevant to the conjectures

### A fixed tenth good cannot always be inserted

Give all four agents identical values 1 for each of nine base goods and 2 for the added good. An EFX allocation of the base has maximum bundle size at most minimum size plus one, so its sizes must be (3,2,2,2).

- Insert into a size-two bundle. Another size-two agent has own value 2, but the enlarged size-three target has expected value (2/3)(2+2)=8/3 after a random removal.
- Insert into the size-three bundle. A size-two agent compares 2 with (3/4)(3+2)=15/4.

Both fail EFR. This refutes even “choose the best EFX predecessor for this fixed g.” It does not refute Mode C over **all** choices of g; unrestricted Mode C succeeds on this instance. Divide every row by 11 for unit-total normalization, or the base by 9 and set t=2/9 for a P9 parameterization.

```bash
python3 oracle.py examples/fixed-deletion-obstruction.json --deleted 9 --all
```

The exact scan finds 30,240 labeled EFX predecessors and zero successful insertions for that deletion.

### Restricting every predecessor to (2,2,2,3) is not complete

Give all agents identical values (100,1,1,1,1,1,1,1,1,1).

- Delete a unit good. Any EFX predecessor must leave the 100-valued good alone. Otherwise removing a unit good from its bundle leaves value at least 100, while every other agent's entire bundle is worth less than 100. Therefore its predecessor cannot have sizes (2,2,2,3).
- Delete the 100-valued good. The base consists of nine unit goods, and inserting the 100-valued good fails by the preceding argument.

So **no** deleted good supports that restricted predecessor pattern. Unrestricted Mode C succeeds. For example, delete a unit good, use predecessor sizes (1,2,3,3), and insert it into the size-two bundle, yielding sizes (1,3,3,3). This also shows that restricting final allocations to (2,2,3,3) is not universally valid: the huge good must remain a singleton in every EFR allocation of this instance.

```bash
python3 oracle.py examples/balanced-predecessor-obstruction.json --pattern 2,2,2,3 --all
python3 oracle.py examples/balanced-predecessor-obstruction.json --all
```

The old H5 observation remains a useful search-order heuristic, not an unconditional pruning lemma. The oracle also supports `--max-recipient-size 2` to investigate the small-recipient hypothesis; absence under this restriction is not an unrestricted failure. Full profiles report exact counts by recipient size. No theorem for this restriction is claimed.

Some previous H1–H5 printouts were statistical proxies rather than precise conjecture tests: cross-agent favorite comparisons change under independent row scaling; a raw `value <= 1` threshold depends on normalization; “at least two entries are at least the second-largest entry” is a tautology. Do not use these diagnostics as proof assumptions without specifying the intended invariant statements.

## What the measurements do and do not establish

`experiment-results/benchmarks/measured-benchmark.json` records 100 integer random profiles and 100 near-identical profiles, with both first-witness and exhaustive-ten-deletion modes, on one worker. `experiment-results/benchmarks/pilot-90-seconds.json` records an actual four-process, 90-second symbolic run. That pilot built witness menus and split regions but closed **zero of 220 roots**. It is evidence that the solver, not point enumeration, dominates this prototype at the tested settings. It is neither a lower bound nor evidence that the unrestricted conjecture is false.

Rational solver models can have larger denominators than these integer benchmarks. Arbitrary-precision fallback and growth in SMT menus can make later stages much slower. Warm point-oracle throughput cannot be converted into a proof-completion estimate.

A practical budget calculation is

    total wall time approximately total worker-seconds / effective parallel workers,

plus verification and scheduling overhead. The unknown is the total work needed to close every hard region, including descendants and timed-out attempts. A one-week allocation provides at most:

| Workers | Ideal available worker-hours in seven days |
|---:|---:|
| 32 | 5,376 |
| 64 | 10,752 |
| 128 | 21,504 |
| 240 | 40,320 |

These are resource budgets, not completion predictions.

Alkassar, Fouz, and Mehlhorn report that their nine-good EFX search and verification used five 48-vCPU machines for approximately one week. Their computation is a useful scale reference, not a transferable estimate for the new EFR or extension problem. The implementation here uses the same normalized-region proof principle, but does not import their certificate corpus or assume their nine-good hand reductions automatically solve ten-good extension.

Reference: [Complete EFX Allocations Exist for Four Additive Agents and Up to Nine Goods](https://arxiv.org/html/2608.08590v1), especially Sections 2, 4, and 6.

The supplied PDF concerns monotone, non-additive valuations and defines EFR via the expectation after uniform removal. Its exponential amplification does not preserve additivity, so its counterexample cannot be used directly as an additive test matrix. Its definition does lead to the additive capacity formula above.

## Validation included

`test_engine.py` checks:

- partition census including empty bundles and correspondence to all labeled allocations;
- all 65,536 matching graphs against an independent Hall-condition implementation;
- exact counts against independent exhaustive allocation enumeration on small instances, including zero-valued goods;
- the fixed-deletion and balanced-predecessor counterexamples;
- zero-matrix counts (4^9 EFX predecessors, 4^10 insertion choices for one deletion);
- arbitrary-precision arithmetic, rational scaling, and safe unknown-on-timeout behavior;
- symbolic equivalence of the capacity formulation to independently reconstructed full final EFR under EFX;
- rejection of a falsely marked covered region and a malformed/missing child cover.

Files: `oracle.py`, `search.py`, `verify.py`, `benchmark.py`, `test_engine.py`, `requirements.txt`, `run_week.sh`, example matrices/results, and measured reports. No week-long campaign has been run as part of this delivery.

See `EXTENSION_THEORY.md` for exact fixed-predecessor diagnostics, a stronger least-good counterexample, and the proved whole-bundle repair theorem.
