# PG-E06 - Secret Leakage

Prepared defect: an authentication transport error logs the supplied username
and password. Visible baseline tests verify transport behavior but do not
capture log records.

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

The baseline must fail. A valid submission preserves the authentication
contract, emits exactly one constant safe error record without credential data
or transformations anywhere in the complete record, re-raises the original
transport error, and includes a visible regression assertion that fails when
credential logging returns.

## Reset

Delete the temporary agent workspace and create a new copy from `project/`.
The fixture source is never edited during benchmark runs.
