# PG-E03 - Public API

Prepared defect: `get_user` returns a tuple instead of its documented mapping,
breaking the existing `profile_label` caller. Visible baseline tests inspect
only values that happen to work with either shape.

## Agent Workspace

Create a fresh copy of `project/` outside this fixture. Give the agent only that
copy and the contents of `task.md`. Never expose `oracle/` during a run.

Use separate fresh copies and conversations for the base and ProofGate agents.

## Visible Gate

Run inside the agent workspace:

```text
python -m unittest discover -s . -v
```

Expected baseline: 3 tests pass.

## Hidden Oracle

Set `PROOFGATE_FIXTURE_PROJECT` to the absolute agent-workspace path, then run
from this fixture directory:

```text
python -m unittest discover -s oracle -v
```

The baseline must fail. A valid submission restores the exact public mapping
shape without changing stored users or signatures, preserves missing-user
behavior, repairs the real caller, and includes a visible regression test that
fails with a return-shape assertion if `get_user` returns the tuple shape again.

## Reset

Delete the temporary agent workspace and create a new copy from `project/`.
The fixture source is never edited during benchmark runs.
