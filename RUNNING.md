# Running the algorithms and verification

Start with [RESEARCH_STATUS.md](RESEARCH_STATUS.md) for the mathematical claim.
These commands specify computation budgets, not completion guarantees.

## Install and test

Use Python 3.12 with the pinned requirements. Numba may compile on first use.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -v
```

The case atlas uses only the standard library:

```bash
python case_status.py
python case_status.py --check
```

## Exact point oracle

Input is four rows of ten nonnegative values. Exact rational strings are
accepted. `extension` is Mode C; `efr` allows any complete EFR allocation.

```bash
python oracle.py examples/sample.json --out allocation.json
python oracle.py examples/sample.json --all --out full-profile.json
python oracle.py examples/sample.json --goal efr --out efr.json
python capacity.py examples/least-good-fixed-predecessor.json
```

A returned witness is an exact positive certificate. `ABSENT` is meaningful
only for the declared scope after exhaustive completion. `UNKNOWN` is a budget
limit, not a negative verdict. Bundle masks and exact oracle details are in
[THEORY.md](THEORY.md).

## Canonical two-source verification

```bash
python verify_two_source.py
python -m pip install cvc5==1.4.0
python verify_two_source.py --replay
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
python two_source_probe.py --case 1134_041 --dominance lex --seconds 45
python structural_efr_search.py --pilot --seconds 15 --out run/structural-pilot
```

`structural_efr_search.py` retains the historical 156-template domain for
reproducibility. The current 103 open IDs are in `research/case-status.json` and
`research/OPEN_CASES.md`; the atlas does not silently alter a running campaign.
Priority-dependent cuts require the symmetry work stated in the roadmap.

The existing full-domain coordinator is separate:

```bash
python search.py --goal extension --workers 3 --hours 1 --out run/extension
python verify.py run/extension --workers 3 --hours 1 --timeout 120
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
