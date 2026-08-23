# PG-E05 - Migration Rollback

Prepared defect: a failure after the first row is migrated leaves a mixture of
old and new schema fields. Visible tests pass on the baseline and cover only a
successful migration.

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

The baseline must fail. A valid submission propagates migration failures,
restores the complete in-memory baseline in place, invokes each `after_row`
callback only after that row has its new schema, still completes successful
migrations, and includes a visible regression test that fails when rollback is
removed.

## Reset

Delete the temporary agent workspace and create a new copy from `project/`.
The fixture source is never edited during benchmark runs.
