# EFR search on GitHub Actions

Upload this repository to GitHub, open **Actions → EFR parallel search → Run workflow**, and the computation will run on GitHub's machines. Your computer can be switched off after the workflow starts.

This is the complete four-agent additive EFX9 → EFR10 research package plus a GitHub workflow. It includes exact rational search, parallel shards, checkpoint artifacts, continuation, independent verification, and an overall progress report. A finished workflow can still mean an unfinished mathematical search.

## 1. Put the files in your repository

Create an empty GitHub repository. Extract `efr_github_ready.zip`; the resulting `efr-github` directory is the repository root. Upload its **contents**, so that GitHub sees:

- `.github/workflows/efr-search.yml`
- `oracle.py`, `search.py`, `verify.py`, `ci.py`
- `requirements.txt`, `test_engine.py`, `test_ci.py`
- `README.md`, `THEORY.md`, and the other supplied files

Do not upload only the ZIP, and do not put the `efr-github` outer directory inside your repository. The workflow must be at the repository root path `.github/workflows/efr-search.yml`.

On a Mac, Finder may hide `.github`. Press **Command + Shift + .** to show it. Pushing with Git includes it automatically:

```bash
cd ~/Downloads/efr-github

git init -b main
git add .
git commit -m "Add exact EFR search and GitHub workflow"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

Replace the repository URL. GitHub may ask you to sign in through your configured Git client. These commands assume a new empty repository; for an existing repository, copy these files into its checkout and commit normally.

There are no API keys, paid solver licenses, or custom secrets to set up. The workflow uses GitHub's built-in token with read permissions and GitHub's artifact service.

## 2. Start the first run

In your repository:

1. Open **Actions**. Enable Actions if GitHub asks.
2. Choose **EFR parallel search**.
3. Click **Run workflow**, with branch `main`.
4. Keep these initial values:

| Field | First run |
|---|---|
| `mode` | `search` |
| `goal` | `extension` |
| `shards` | `4` |
| `minutes` | `15` |
| `resume_run` | Leave empty |

The prepare job checks the inputs, installs the pinned dependencies, and runs all 19 unit tests. Four independent jobs then each search for up to 15 minutes, perform up to five minutes of independent verification, and upload their checkpoint. Setup, queueing, and uploads add time.

After a successful initial round, you can run longer rounds with `minutes = 270` (4.5 hours of search per shard). Each job is bounded below GitHub's hosted-job time limit, with room for verification and artifact uploads.

Choose your desired shard count **when starting a campaign**. To use 20 parallel jobs immediately, set `shards = 20` on the first run. To change from four shards to twenty later, start a new campaign with an empty `resume_run`; redistribution of existing checkpoints is not implemented. Parallel jobs may queue if your account has fewer free execution slots.

The worker count is selected automatically: up to three search processes on a four-CPU runner, or one on a two-CPU runner. Each solver process uses one thread.

## 3. Continue the same search

Checkpoints are restored automatically **after you specify the source run ID**. The workflow does not autonomously schedule another round.

Once the first workflow run has finished:

1. Open its Summary. The overall report includes the numeric run ID to use next.
2. Alternatively, take the number from the URL:
   `https://github.com/OWNER/REPO/actions/runs/12345678901` → `12345678901`.
3. Click **Run workflow** again.
4. Keep the **same goal and shard count**.
5. Set `resume_run` to that numeric ID and choose a new time budget.

Each job downloads only its own shard's compressed checkpoint from that run, verifies the code/goal/sharding identity, restores it, and continues. The new round uploads a new set of artifacts. Use the **newest completed round's ID** next time.

Leaving `resume_run` empty starts a fresh search. The GitHub **Re-run jobs** button repeats the old inputs; use **Run workflow** with the new source ID when you want to continue from the newest checkpoints.

A checkpoint is intentionally rejected if `oracle.py`, `search.py`, `verify.py`, `requirements.txt`, or `ci.py` has changed. This prevents results from incompatible mathematical implementations being silently combined. Documentation or workflow-only changes do not alter that fingerprint.

## 4. Read the results

Open the completed workflow's **Summary**. It shows the progress of each shard and the ID needed to resume. At the bottom of the page, the **Artifacts** section contains:

- `efr-extension-n4-s0`, etc.: `checkpoint.tar.gz` and `result.json` for each shard. These are the files needed to resume or move the computation to another machine.
- `report-efr-extension-n4-s0`, etc.: small reports for the summary job. The summary job downloads these, not all large checkpoints.
- `campaign-report`: `campaign-summary.json` and `campaign-summary.md`.

The names reflect your selected goal/shard count.

| Result | Meaning |
|---|---|
| `INCOMPLETE_NO_THEOREM` | Search or verification still has uncovered/unverified regions. Resume or allow more time. |
| `ALL_SHARDS_VERIFIED` | All required shards independently verified all their assigned root regions in this run, under the same code and mathematical goal. |
| `COUNTEREXAMPLE_REQUIRES_RECHECK` | The search found an exact negative instance for the selected construction/goal; inspect the node's saved valuation and oracle record. |
| `ERROR`, missing shard, or failed restore | An execution/configuration problem; inspect job logs before continuing. |

**A green GitHub workflow is not an existence theorem.** A run with incomplete research progress can legitimately be green. Only the stated verifier result certifies coverage. Verification trusts Z3's UNSAT answers; no independently checked formal proof objects are produced.

For `goal = extension`, the claim is existence of some deleted good, some complete EFX0 predecessor on the remaining nine goods, and a capacity-feasible insertion yielding EFR. For `goal = efr`, the claim is final EFR existence, which is weaker than universal success of the predecessor construction. `efx9` searches the established nine-good EFX existence question.

## 5. Give verification its own longer run

Search mode allows five minutes of verification per shard after each search interval. To spend a full interval replaying certificates independently, run:

| Field | Verification round |
|---|---|
| `mode` | `verify` |
| `goal` | Same as the campaign |
| `shards` | Same as the campaign |
| `minutes` | Up to `270` |
| `resume_run` | Latest completed run ID |

Verification uses fresh solver instances. It does not carry unfinished solver state between rounds. It verifies the checkpoint independently rather than assuming the search's `COVERED` labels are true.

## Costs, persistence, and failures

Standard GitHub-hosted runner compute is free for public repositories. Private repositories consume your plan's included minutes and may incur charges afterward. A 20-job, 270-minute search uses about **5,400 runner-minutes**, plus setup and verification. Artifact storage has separate limits.

Artifacts in this workflow are retained for **14 days**. Download backups before expiry. If an artifact is missing, expired, or incompatible, the resume step fails explicitly; it does not silently start that shard over. Monitor your artifact quota during longer campaigns. Older rounds are not automatically deleted.

The workflow normally saves artifacts after the bounded search finishes. A manual cancellation, runner crash, or out-of-memory failure can lose work since the previous uploaded checkpoint. If a job fails before uploading, the preceding completed round is still the recovery point. Inspect the logs or re-run failed jobs before using an incomplete run as the next source.

No weekly completion estimate is promised. The search can be continued in these bounded rounds, but the hardest regions may need new mathematical reductions. The supplied local pilot did not prove a whole-space result.

GitHub references:

- [Runner specifications](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)
- [Actions limits](https://docs.github.com/en/actions/reference/limits)
- [Artifact upload action](https://github.com/actions/upload-artifact)
- [Downloading artifacts with GitHub CLI](https://cli.github.com/manual/gh_run_download)

## Local execution and mathematical details

The Python programs also work outside GitHub:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m unittest -v test_engine test_ci
python3 oracle.py examples/sample.json --out allocation.json
```

Read **THEORY.md** for the capacity lemma, exact matching acceleration, normalization, counterexamples to restricted constructions, benchmark interpretation, and the search/verifier design.

Local validation covers the 19 tests, workflow YAML and shell syntax, and a real short search → archive → restore → continued-search cycle. This package has not been deployed or run on your GitHub account from this chat.
