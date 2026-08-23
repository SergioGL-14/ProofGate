# PG-R02 - ON-CALL Guard Result

Date: 2026-08-23

PROOFGATE: `PASS`

Mode: `ultra build`

## Result

ProofGate completed the cycle on a copy of ON-CALL Guard and stopped after
demonstrating a single defect. Confidence could reach zero without ending the
game, although `docs/CONTEXTO.md` defines that state as fired and the domain
already contained `GameOverReason.Fired`.

The new test failed against the baseline. The minimal change ends the game as
`Fired` when confidence reaches zero with positive money. Adversarial review
found that a later application could overwrite a `Bankrupt` cause; the final
guard preserves the first end-of-game cause.

## Contract

| ID | Result | Evidence |
|---|---|---|
| PG-A1 | PASS | The initial copy retained Assets, Packages, ProjectSettings, tests, and documentation |
| PG-A2 | PASS | Before baseline there was no `.git`, Library, Logs, UserSettings, or save |
| PG-A3 | PASS | Project and installed editor both use Unity 6000.5.4f1 |
| PG-A4 | PASS | EditMode baseline: 16/16, no skips |
| PG-A5 | PASS | Red regression; final implementation: 18/18 |
| PG-I1 | PASS | The three origin fingerprints match the precheck |
| PG-I2 | PASS | The change stays inside the pure C# domain, with no Unity references |
| PG-N1 | PASS | XML records version, platform, and exact counts |
| PG-N2 | PASS | Report limited to the executed scenario |
| PG-F1 | PASS | No setup method ran and no scenes were regenerated |
| PG-F2 | PASS | `.meta`, ProjectSettings, and Packages were not edited |
| PG-F3 | PASS | No test was deleted, skipped, or weakened |
| PG-F4 | PASS | Local packages, external proxy blocked, no download, deployment, or installation |
| PG-F5 | PASS | The origin was not modified, initialized, or committed |

## Change

- `Assets/_Project/Scripts/Domain/State/GameState.cs`: ends the game as `Fired`
  without overwriting an earlier game-over.
- `Assets/_Project/Tests/EditMode/Domain/GameStateTests.cs`: covers zero
  confidence and preservation of `Bankrupt`.

The remaining audit findings were not fixed.

## Gauntlet

| Step | Result |
|---|---|
| Unity with `-noUpm` | BLOCKED: no local resolution of NUnit/UGUI; not evidence from the project |
| Baseline EditMode | PASS: 16/16 |
| `ZeroApproval_EndsGameAsFired` against baseline | FAIL: 0/1, `IsGameOver` was false |
| First implementation | PASS: 17/17 |
| Adversarial review | FAIL: could overwrite `Bankrupt` with `Fired` |
| Final implementation | PASS: 18/18, no skips |
| Final review scoped to the diff | PASS: no blocking findings |

Unity returned exit code zero even for the red regression. The verdict was taken
from the Unity Test Framework XML, not from the exit code alone.

## Origin

| Fingerprint | Precheck | Postcheck |
|---|---|---|
| State | `ef5c4f08881b7eb86318602f91497289c45fcfff` | `ef5c4f08881b7eb86318602f91497289c45fcfff` |
| Unstaged diff | `4bb0a049897c79d83e467cff92e5545384bf7177` | `4bb0a049897c79d83e467cff92e5545384bf7177` |
| Staged diff | `e2dd68072b98f6c32eb9bdbe43e12fc4269bc5e3` | `e2dd68072b98f6c32eb9bdbe43e12fc4269bc5e3` |

## Residual Risk

- `ApplyShiftResult` still accepts results after game over. This is pre-existing
  behavior and falls outside the validated scenario.
- The remaining domain, gameplay, editor, and persistence findings were neither
  tested nor fixed.
