# Running the algorithms and verification

Start with [RESEARCH_STATUS.md](RESEARCH_STATUS.md) for the mathematical claim.
These commands specify computation budgets, not completion guarantees.

## Install and test

Run commands from the repository root. Code is in `efr/`, tests in `tests/`,
and the optional week wrapper in `scripts/run_week.sh`. Use Python 3.12 with the pinned requirements. Numba may compile on first use.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -v
```

The case atlas uses only the standard library:

```bash
python -m efr.case_status
python -m efr.case_status --check
```

## Exact point oracle

Input is four rows of ten nonnegative values. Exact rational strings are
accepted. `extension` is Mode C; `efr` allows any complete EFR allocation.

```bash
python -m efr.oracle examples/sample.json --out allocation.json
python -m efr.oracle examples/sample.json --all --out full-profile.json
python -m efr.oracle examples/sample.json --goal efr --out efr.json
python -m efr.capacity examples/least-good-fixed-predecessor.json
```

A returned witness is an exact positive certificate. `ABSENT` is meaningful
only for the declared scope after exhaustive completion. `UNKNOWN` is a budget
limit, not a negative verdict. Bundle masks and exact oracle details are in
[THEORY.md](THEORY.md).

## Canonical two-source verification

```bash
python -m efr.verify_two_source
python -m pip install cvc5==1.4.0
python -m efr.verify_two_source --replay
```

The first command reads the canonical verified obstruction, independently
enumerates all two-agent repartitions, checks its nondegenerate refinement,
and reproduces three-agent and Mode C witnesses. It does not need exploratory
probe logs. The replay rebuilds the 50 compensation formulas and loads the
three retained finite-menu formulas. It writes 53 portable SMT2 inputs under
`run/verification/portable/`, then checks them with cvc5 proof
checking enabled. Generated portable inputs are ignored by git; the generator,
canonical source inputs, and replay records are retained. New verification
reports go to `run/verification/` without overwriting the canonical evidence.

## Optional bounded research probes

These can find examples or partial covers. They are not necessary to reproduce
the case atlas, and no long run is started automatically.

```bash
python -m efr.two_source_probe --case 1134_041 --dominance lex --seconds 45
python -m efr.structural_efr_search --pilot --seconds 15 --out run/structural-pilot
```

`efr/structural_efr_search.py` retains the historical 156-template domain for
reproducibility. The current 102 open IDs are in `research/case-status.json` and
`research/OPEN_CASES.md`; the atlas does not silently alter a running campaign.
Priority-dependent cuts require the symmetry work stated in the roadmap.

The existing full-domain coordinator is separate:

```bash
python -m efr.search --goal extension --workers 3 --hours 1 --out run/extension
python -m efr.verify run/extension --workers 3 --hours 1 --timeout 120
```

Reusing a compatible output directory resumes its checkpoint. Do not reuse a
directory for another goal or run two coordinators against one directory.
The independent verifier must certify all required regions before a whole-space
claim is made. A time cutoff only bounds the attempt.

## Existing GitHub workflows

Use the research branch `improve-search-and-capacity-theory` when inspecting or
manually dispatching its workflows. Main is not changed by this research cleanup.

| Workflow file | Scope |
| --- | --- |
| `.github/workflows/efr-search.yml` | Full normalized-domain coordinator; `extension`, `efr`, or `efx9`; resumable shards. |
| `.github/workflows/exchange-experiment.yml` | Finite exchange-graph experiments, not an existence proof. |
| `.github/workflows/rebundle-experiment.yml` | Finite minimum-distance experiments. |

For the parallel workflow, keep the same goal and shard count when resuming;
set `resume_run` to the newest completed compatible run ID. An empty value
starts a new campaign. The workflow does not schedule further rounds itself.
Changes to the mathematical implementation can invalidate old checkpoints.
The current workflow retains uploaded artifacts for 14 days; repository
evidence is retained separately.

`INCOMPLETE_NO_THEOREM` means that coverage or verification is unfinished.
`ALL_SHARDS_VERIFIED` is the declared full-cover result under the selected goal
and verifier assumptions. A green workflow alone establishes neither.

The package reorganization changes the workflow code fingerprint. Existing campaign
archives must be resumed on their original compatible commit; the identity check
is intentionally not bypassed. Exchange and rebundling workflows are now manual-only.

## Fixed-priority local compensation

`efr.compensation.compensated_relay` checks one proposed safe champion bundle;
`pair_relays` checks only the proved pair specialization. Both accept an explicit
agent priority. A returned certificate is an EFX improvement; no result does not
mean no repair exists. See [the proof](research/SOURCE_COMPENSATION.md).

```bash
python -m efr.priority --out research/priority-cases.json
python -m unittest -v tests.test_compensation
```

The priority generator enumerates finite graph symmetries, not valuations.
