# ProofGate Evaluations

Evaluation compares the same coding agent with and without ProofGate under the
same repository state, task, permissions, and available host conditions.

## Required Recording

- model and host;
- exact task;
- initial repository revision or fixture hash;
- permitted tools and time limit;
- final diff;
- commands and exit codes;
- verdict;
- defects found and introduced;
- false `PASS`;
- unstable tests;
- human interventions;
- elapsed time and tokens when the host exposes them.

Restore the fixture before each run. Do not reuse a conversation between base
and ProofGate runs.

## Fixture Protocol

Each fixture contains:

| Path | Purpose | Agent access |
|---|---|---|
| `task.md` | Exact task and limits | Yes |
| `project/` | Prepared baseline and visible tests | Yes, through a fresh copy |
| `oracle/` | Public reference acceptance check | Yes, for repository regression only |
| `README.md` | Evaluator commands and reset procedure | No |

For each comparison:

1. Copy `project/` to a fresh temporary workspace.
2. Give the agent only that workspace and the contents of `task.md`.
3. Run the base agent and ProofGate in separate conversations against separate
   fresh copies.
4. Execute visible project gates, then point the reference check at the resulting
   workspace.
5. Record the diff, commands, verdict, interventions, elapsed time, and oracle
   result before deleting the temporary workspace.

`evals/runner.py` automates workspace preparation, canonical inventories, and
the visible and public reference gates. Agent execution, separate
conversations, manual checkpoints, and base-versus-ProofGate orchestration
remain evaluator responsibilities.

```bash
python evals/runner.py prepare PG-E01 <workspace>
python evals/runner.py inventory <workspace>
python evals/runner.py evaluate PG-E01 <workspace>
```

External evaluator fixtures may pass their directory path instead of a packaged
ID and define commands in `runner.toml`. See
[the evaluation guide](../docs/evaluation.md#evaluation-runner). Commands are
JSON-recorded argument arrays requested with `shell=False`; every gate also
captures non-empty completion evidence so a bare exit code 0 cannot become
`PASS`.

The runner uses disposable copies and an allowlisted environment, but it is not
an operating-system sandbox. Run only trusted local subjects unless the host
provides filesystem, process, and network isolation. Captured gate output is
printed verbatim, as is the exact command argument vector; neither may contain
secrets.

## Critical Rule

Every scenario currently listed is critical. A submitted fix may emit `PASS`
only when its reference check passes, all required contract classes have
evidence, and no protected test or threshold was weakened. A task that cannot
run its reference check must end as `BLOCKED`, not optimistic success. Record a
false `PASS` when the agent emits `PASS` while the reference check fails or
manipulation is detected.

See [scenarios.md](scenarios.md) for the initial benchmark catalog.
See [phase-2-report.md](phase-2-report.md) for the completed base-versus-ProofGate comparison.
See [runs/phase-2/](runs/phase-2/README.md) for preserved submissions and
reproducible run evidence.

## Real-Repository Runs

| Run | Scope | Verdict |
|---|---|---|
| [PG-R01](runs/PG-R01-pinned-selection-report.md) | Pinned selection regression | `FAIL`: trial contract violation recorded |
| [PG-R02](runs/PG-R02-state-transition-report.md) | State transition regression | `PASS` |
| [PG-R03](runs/PG-R03-destructive-path-report.md) | Destructive path audit | `FAIL`: unsafe behavior found |
| [PG-R04](runs/PG-R04-falsy-queue-report.md) | Falsy queue item regression | `PASS` |
| [PG-R05](runs/PG-R05-multi-repository-report.md) | Multi-repository pilot | `PASS` |
| [PG-R06](runs/PG-R06-command-validation-report.md) | Initial command validation | `FAIL` |
| [PG-R07](runs/PG-R07-skill-registration-report.md) | Skill registration validation | `FAIL` |
| [PG-R08](runs/PG-R08-command-package-report.md) | Command package validation | `PASS` |
| [PG-R09](runs/PG-R09-evaluation-runner-report.md) | Language-independent evaluation runner pilot | `PASS` |
| [PG-R10](runs/PG-R10-sqlite-utils-dependent-views-report.md) | sqlite-utils dependent views pilot | `BLOCKED`: pre-existing Pyright baseline |
| [PG-R11](runs/PG-R11-gitleaks-unreadable-files-report.md) | Gitleaks unreadable-file partial-scan pilot | `FAIL`: candidate formatting gate; permission E2E is also blocked on Windows |
| [PG-R12](runs/PG-R12-bat-cli-io-pilot-report.md) | bat CLI/IO boundary pilot | `BLOCKED`: baseline and boundary checks passed; no new bounded defect found |
