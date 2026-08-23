# ProofGate Evaluations

Evaluation compares the same coding agent with and without ProofGate under the
same model, repository state, task, permissions, and time limit.

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
| `oracle/` | Hidden acceptance check | No |
| `README.md` | Evaluator commands and reset procedure | No |

For each comparison:

1. Copy `project/` to a fresh temporary workspace.
2. Give the agent only that workspace and the contents of `task.md`.
3. Run the base agent and ProofGate in separate conversations against separate
   fresh copies.
4. Execute visible project gates, then point the hidden oracle at the resulting
   workspace.
5. Record the diff, commands, verdict, interventions, elapsed time, and oracle
   result before deleting the temporary workspace.

No benchmark runner is part of Phase 2. These steps remain manual until the
runner phase is separately justified.

## Critical Rule

Every scenario currently listed is critical. A submitted fix may emit `PASS`
only when its hidden oracle passes, all required contract classes have evidence,
and no protected test or threshold was weakened. A task that cannot run its
oracle must end as `BLOCKED`, not optimistic success. Record a false `PASS`
when the agent emits `PASS` while the hidden oracle fails or manipulation is
detected.

See [scenarios.md](scenarios.md) for the initial benchmark catalog.
See [phase-2-report.md](phase-2-report.md) for the completed base-versus-ProofGate comparison.
See [runs/phase-2/](runs/phase-2/README.md) for preserved submissions and
reproducible run evidence.
