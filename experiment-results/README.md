# Retained research evidence

This directory contains canonical witnesses, proof inputs, and compact historical
summaries. The current mathematical status is [RESEARCH_STATUS.md](../RESEARCH_STATUS.md),
with a generated [case atlas](../CASE_ATLAS.md). A historical SAT model, timeout,
or failed restricted move is not an overall EFR counterexample.

## Evidence by claim

| Location | Retained evidence | Role |
| --- | --- | --- |
| [two-source/verified-obstruction.json](two-source/verified-obstruction.json) | Small and nondegenerate matrices; two independent enumeration summaries; three-agent and Mode C witnesses. | Canonical N6 counterexample to two-agent fixed-priority repair. |
| [two-source/all-compensation.json](two-source/all-compensation.json) | Historical 156 region definitions and outcomes; exploratory SAT valuations removed. | Selects the 50 CP1 replay inputs; SAT is not a no-EFR verdict. |
| [two-source/cvc5-replay.json](two-source/cvc5-replay.json) | 53 distinct UNSAT replay records, input hashes, solver version, proof-check setting. | Canonical CP1/CP2 replay results. Portable filenames identify generated inputs, not missing committed files. |
| `two-source/2223_{003,011,013}-pareto.json` and matching `.smt2` files | Three successful finite-cover menus and their exact source formulas. | CP2 continuous-region coverage; these are proof inputs, not disposable intermediates. |
| [two-source/reduction-summary.json](two-source/reduction-summary.json) | Historical-156 reduction counts and the 103 open IDs. | Cross-check for the generated atlas. |
| [structural-reduction/catalog.json](structural-reduction/catalog.json) | Earlier 156-template catalog. | Historical baseline, intentionally distinct from the current atlas. |
| [structural-reduction/four-source-example.json](structural-reduction/four-source-example.json) | Blocked four-source start and escape. | Demonstrates that four sources can exist initially; T9 excludes terminal states. |
| [structural-reduction/benchmark-summary.json](structural-reduction/benchmark-summary.json) and three `structural-*-pilot/summary.json` reports | Compact timings and outcomes of bounded local pilots. | Runtime evidence, not a proof-completion estimate. |
| [restoration/](restoration/) | Earlier source-path obstructions and verified escapes. | Regression evidence for the progression to stronger moves. |
| [run-35576951293/](run-35576951293/) | GitHub exchange-run summary and exactly verified traps. | N4 and finite exchange experiment. |
| [run-35597667294/](run-35597667294/) | GitHub rebundling-run summary and reproduced witnesses. | N5 experiments; universal lower bound has a separate human proof. |
| [mode-c-adversary/](mode-c-adversary/) | Aggregate adversarial outcomes, mutation results, singleton regression. | Exploratory evidence; UNKNOWN remains UNKNOWN. |
| [benchmarks/](benchmarks/) | Original point-oracle measurements and 90-second whole-domain pilot summary. | Preserved historical performance evidence. |

## Cleanup performed on 25 September 2026

Removed **31 tracked intermediate files**: 19 completed-pilot witness-menu files,
8 exploratory two-agent probe logs superseded by the canonical verified example,
one duplicate balanced-profile probe report, two duplicate four-source replay
artifacts, and one stale initial-validation snapshot. The two root benchmark
reports were moved here under `benchmarks/`.

Also removed 80 local generated files: raw duplicate pilot outputs, portable
solver regenerations, and uncommitted exploratory candidate logs. They are not
the retained canonical certificates. All deleted committed content remains
recoverable in Git history before this cleanup.

The canonical replay record was deduplicated from 54 checks to 53 distinct
regions. The removed check repeated the four-source region already covered by
the compensation input and by the human proof T9. No distinct closed region
or final verified counterexample was removed.

## Reproduction and future outputs

From the repository root:

```bash
python case_status.py --check
python verify_two_source.py
python verify_two_source.py --replay
```

The optional replay requires `cvc5==1.4.0`. It regenerates portable formulas
under `run/verification/portable/` and saves new reports under `run/verification/`.
Two-source probes and structural pilots likewise default to `run/`. This avoids
overwriting canonical evidence or adding every new scratch result to git.

Retain a new artifact here when it supports a named claim, an exact negative
scope verdict, a verified positive witness, a continuous-region certificate,
or a compact benchmark conclusion. Keep temporary solver models and duplicate
serializations under `run/` instead.

Post-cleanup validation: all 49 tests passed; the atlas regenerated exactly;
all 53 canonical regions replayed UNSAT with cvc5 proof checking enabled; and
the independent 8,532-assignment obstruction verification and positive escape
witnesses were reproduced. Only verification was rerun, not a new valuation
search.
