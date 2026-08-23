# PG-E01 - Boundary Bug

Prepared defect: `MAX_BATCH_SIZE` is documented as inclusive but the exact
maximum is rejected. Visible tests pass on the baseline and omit that boundary.

## Agent Workspace

Create a fresh copy of `project/` outside this fixture. Give the agent only that
copy and the contents of `task.md`. Never expose `oracle/` during a run.

Use separate fresh copies and conversations for the base and ProofGate agents.

## Visible Gate

Run inside the agent workspace:

```text
python -m unittest discover -s . -v
```

Expected baseline: 4 tests pass.

## Hidden Oracle

Set `PROOFGATE_FIXTURE_PROJECT` to the absolute agent-workspace path, then run
from this fixture directory:

```text
python -m unittest discover -s oracle -v
```

The baseline must fail. A valid submission preserves the maximum value of 100,
accepts that exact maximum, rejects values outside 1 through 100, and includes a
visible regression test that fails when the exact-maximum behavior is mutated.

## Reset

Delete the temporary agent workspace and create a new copy from `project/`.
The fixture source is never edited during benchmark runs.
