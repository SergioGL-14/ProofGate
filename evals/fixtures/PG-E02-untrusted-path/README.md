# PG-E02 - Untrusted Path

Prepared defect: containment is checked before URL percent-decoding, so an
encoded parent segment can read a file outside the workspace. Visible tests
pass on the baseline and cover only ordinary paths and literal traversal.

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

The baseline must fail. A valid submission preserves the public contract,
decodes exactly once before real-path containment checking, rejects literal,
encoded, resolved-link, and shared-prefix sibling escapes, permits encoded
names inside the workspace, and includes a visible regression assertion that
fails when the encoded-traversal defect returns.

## Reset

Delete the temporary agent workspace and create a new copy from `project/`.
The fixture source is never edited during benchmark runs.
