# PG-E04 - Concurrent Update

Prepared defect: worker threads read the same counter value before either
writes, so one update is deterministically lost. Visible tests pass on the
baseline and cover only a single update.

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

The baseline must fail. A valid submission preserves every concurrent update,
performs one atomic read-modify-write per delta in worker threads, handles an
empty update set, and includes a visible regression test that fails when stale
reads are restored. Writing a precomputed final total from every worker is not
an atomic update and is rejected.

## Reset

Delete the temporary agent workspace and create a new copy from `project/`.
The fixture source is never edited during benchmark runs.
