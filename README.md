# EFR on top of EFX

Research on four agents, ten indivisible goods, and nonnegative additive
valuations: start from EFX on nine goods and seek an EFR allocation of all ten.
All EFX statements use EFX0, including deletion of zero-valued goods.

**Current status:** no counterexample to unrestricted EFR existence or Mode C
has been found, and neither universal statement has been proved here. The
extremal-obstruction route has **103 open structural templates: 94 with two
sources and 9 with three sources**. A completed workflow is not a completed proof.

## Read the research

| Document | Purpose |
| --- | --- |
| [Research status and roadmap](RESEARCH_STATUS.md) | Consolidated findings, numbered theorem register, refuted claims, and theoretical next steps. |
| [Case atlas](CASE_ATLAS.md) | All 18 size profiles and 1,344 canonical acyclic graph cases; every cell names its theorem/proposition or says **OPEN**. |
| [Open cases](research/OPEN_CASES.md) | Exact IDs, envy edges, and source sets for the 103 unresolved cases. |
| [Latest coordinated-source proofs](TWO_SOURCE_PROGRESS.md) | Four-source progress, a nondegenerate two-agent trap, and a three-agent escape. |
| [Evidence index](experiment-results/README.md) | Retained witnesses, certificate inputs, benchmarks, and cleanup policy. |
| [Running and verification](RUNNING.md) | Installation, point oracles, certificate replay, and existing workflows. |

`T` labels denote human proofs; `CP` labels denote computer-checked propositions.
The atlas excludes **terminal extremal obstructions**. It does not claim that
every EFX starting allocation in a closed row directly accepts the omitted good.
The 103 templates are not the older campaign's 220 valuation-ranking roots.

## Reproduce the status tables

The atlas is generated from exact graph enumeration and retained evidence; this
does not launch a search or require solver packages:

```bash
python case_status.py
python case_status.py --check
```

For algorithms and targeted correctness checks:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -v
python oracle.py examples/sample.json --out allocation.json
```

The optional cross-solver replay requires `cvc5==1.4.0`; see [RUNNING.md](RUNNING.md).
No complete three-to-four-day search runtime has been established.

## Detailed proof notes and code

- [EXTENSION_THEORY.md](EXTENSION_THEORY.md): exact capacities, fixed-deletion failures, common-least-good repair.
- [EXCHANGE_FINDINGS.md](EXCHANGE_FINDINGS.md): certified ownership/exchange traps and their invariant.
- [REBUNDLING_LEMMAS.md](REBUNDLING_LEMMAS.md): distance-five lower bound and the open upper-bound conjecture.
- [RESTORATION_LEMMAS.md](RESTORATION_LEMMAS.md): imported BCFF restoration, unique-source progress, and boundary handling.
- [STRUCTURAL_REDUCTIONS.md](STRUCTURAL_REDUCTIONS.md): the historical reduction to 156 cases, strengthened by the current atlas.
- [MODE_C_ADVERSARY_FINDINGS.md](MODE_C_ADVERSARY_FINDINGS.md): finite exploratory searches, not coverage certificates.
- [THEORY.md](THEORY.md): normalization, matching-based exact oracle, and continuous-region search architecture.

The core oracle/search files, research move implementations, regression tests,
and manually dispatched workflows remain at their existing paths. Older run
summaries are explicitly historical; the research status and case atlas are
the current navigation point.
