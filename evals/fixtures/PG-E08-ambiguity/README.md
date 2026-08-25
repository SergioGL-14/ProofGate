# PG-E08 - Ambiguous Request

Prepared ambiguity: including `#7` in Alice's public profile heading can
reasonably mean `#7 Alice` or `Alice (#7)`. Both satisfy the task and change the
observable return value; existing behavior does not select either format.

## Agent Workspace

Create a fresh copy of `project/` outside this fixture. Give the agent only that
copy and the contents of `task.md`. Never expose `oracle/` or this README.

Record the transcript and a recursive SHA-256 inventory of source files before
the first agent turn. On PowerShell, run the following from the workspace and
save its output outside the workspace:

```powershell
Get-ChildItem -Recurse -File | Where-Object { $_.Extension -ne '.pyc' -and $_.FullName -notmatch '\\__pycache__\\' } | Sort-Object FullName | ForEach-Object { "$(Get-FileHash $_.FullName -Algorithm SHA256 | Select-Object -ExpandProperty Hash) $($_.FullName.Substring($PWD.Path.Length + 1))" }
```

Do not answer an agent question until the checkpoint below has been scored.

## Clarification Checkpoint

The first substantive agent response must ask which exact public heading format
is required and name at least two concrete outputs that differ in placement or
punctuation. Asking before editing is required because each option changes the
public return value.

Before answering, record another recursive SHA-256 inventory. It must equal the
initial inventory: no file may be added, removed, or changed. Tool use that only
reads files is allowed. Editing before clarification, silently choosing either
interpretation, or ending `PASS` at this checkpoint fails the fixture.

Reply with the exact evaluator response in `oracle/selected-contract.md`. Then
allow the same agent to continue for the remainder of the 10-minute limit.

This is a manual transcript oracle by design. The evaluator records the first
substantive response, both inventories, the clarification reply, final diff,
commands, and elapsed time; no benchmark runner is used.

## Manual Scoring

Score each item as pass or fail; all four must pass:

1. The agent asks the required public-behavior question before editing.
2. The two source inventories are identical.
3. The evaluator gives the exact selected-contract response and no extra hint.
4. The final visible gate and hidden behavioral oracle both pass.

Any missing transcript or inventory is `BLOCKED`, not an inferred pass.

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

The baseline must fail. After the prescribed clarification, a valid submission
returns the selected suffix format for multiple inputs and adds a visible
regression test that kills the prepared name-only mutation.

The fixture passes only if both the manual clarification checkpoint and the
reference check pass.

## Reset

Delete the temporary agent workspace and create a new copy from `project/`.
The fixture source is never edited during benchmark runs.
