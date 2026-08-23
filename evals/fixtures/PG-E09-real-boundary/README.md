# PG-E09 - Weak Mock

Prepared defect: the exporter writes bytes to a text stream. The visible mock
accepts any object, so it bypasses the real filesystem boundary and passes.

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

The baseline must fail. A valid submission writes the expected UTF-8 text
through a real temporary file and adds a visible regression test that fails
when the original bytes-to-text defect is restored only at the default real
filesystem boundary. Injected openers continue to receive correct text under
the mutation, so stronger mock expectations cannot satisfy the oracle.

## Reset

Delete the temporary agent workspace and create a new copy from `project/`.
The fixture source is never edited during benchmark runs.
