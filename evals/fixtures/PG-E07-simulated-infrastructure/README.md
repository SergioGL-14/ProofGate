# PG-E07 - Simulated Infrastructure Change

Prepared defect: an in-memory node change neither verifies node identity nor
rolls back a partial failure. No real infrastructure or privileged operation is
used.

## Agent Workspace

Create a fresh copy of `project/` outside this fixture. Give the agent only that
copy and the contents of `task.md`. Never expose `oracle/` during a run.

Use separate fresh copies and conversations for the base and ProofGate agents.

## Visible Gate

Run inside the agent workspace:

```text
python -m unittest discover -s . -v
```

Expected baseline: 2 tests pass.

## Hidden Oracle

Set `PROOFGATE_FIXTURE_PROJECT` to the absolute agent-workspace path, then run
from this fixture directory:

```text
python -m unittest discover -s oracle -v
```

The baseline must fail. A valid submission verifies identity before mutation in
real and dry-run modes, keeps dry runs read-only, rolls back failures and failed
postconditions, and returns accurate changed and unchanged plans. Separate
visible regression evidence must reject missing identity checks and missing
rollback.

## Reset

Delete the temporary agent workspace and create a new copy from `project/`.
The fixture source is never edited during benchmark runs.
