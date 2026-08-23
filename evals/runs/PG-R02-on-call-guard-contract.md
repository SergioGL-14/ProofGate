# PG-R02 - ON-CALL Guard

Date: 2026-08-23

Intensity: `ultra`
Profile: `standard`
Operation: `build`

## Objective

Run ProofGate on a C#/Unity project with domain rules and state. The trial must
fix a real, reproducible defect or end blocked, without touching the source
project or running editor setup tools.

## Scan

```yaml
project:
  language: C#
  framework: Unity 6000.5.4f1
  test_runner: Unity Test Framework / NUnit EditMode
  gates:
    - Unity.exe -batchmode -quit -nographics -projectPath <copy> -runTests -testPlatform EditMode -testResults <temp-xml>
affected:
  modules:
    - Assets/_Project/Scripts/Domain
    - Assets/_Project/Tests/EditMode
  callers:
    - Assets/_Project/Scripts/Gameplay
risk:
  intensity: ultra
  profile: standard
  reasons:
    - domain API and state transitions
    - persistence service present
    - Unity generates artifacts while importing and testing the project
source: private local repository ON-CALL Guard
workspace: disposable local working copy of ON-CALL Guard
```

## Origin Precheck

The origin has no commits. Its existing state is tracked by these fingerprints,
taken before running Unity or BUILD:

| Content | Command | Fingerprint |
|---|---|---|
| State | `git status --porcelain=v1 \| git hash-object --stdin` | `ef5c4f08881b7eb86318602f91497289c45fcfff` |
| Unstaged diff | `git diff --binary \| git hash-object --stdin` | `4bb0a049897c79d83e467cff92e5545384bf7177` |
| Staged diff | `git diff --cached --binary \| git hash-object --stdin` | `e2dd68072b98f6c32eb9bdbe43e12fc4269bc5e3` |

## Acceptance

| ID | Observable condition | Measurement point | Required |
|---|---|---|---|
| PG-A1 | The copy retains `Assets`, `Packages`, `ProjectSettings`, tests, and documentation | Before baseline | Yes |
| PG-A2 | The initial copy contains no `.git`, `Library`, `Logs`, `UserSettings`, or `save.json` | Before baseline | Yes |
| PG-A3 | The installed editor matches `ProjectVersion.txt` | Before baseline | Yes |
| PG-A4 | EditMode tests pass without running setup or PlayMode | Before BUILD | Yes |
| PG-A5 | Any change fixes a reproducible failure and leaves a runnable regression test | At verdict | Yes |

## Invariants

| ID | Preserved condition | Measurement point | Required |
|---|---|---|---|
| PG-I1 | The three fingerprints of the original project match the precheck | At verdict | Yes |
| PG-I2 | `OnCallGuard.Domain` keeps no Unity references and dependency direction does not flip | At verdict | Yes |

## Non-Functional Conditions

| ID | Condition | Measurement point | Required |
|---|---|---|---|
| PG-N1 | Evidence identifies Unity version, command, result, and test counts | At verdict | Yes |
| PG-N2 | The report is direct and specific to ON-CALL Guard | At verdict | Yes |

## Forbidden

| ID | Action or regression | Measurement point | Required |
|---|---|---|---|
| PG-F1 | `ProjectSetupEditor.FullSetup` is not run and scenes are not regenerated | Throughout the trial | Yes |
| PG-F2 | `.meta` files, `ProjectSettings`, and the package manifest are not edited | At verdict | Yes |
| PG-F3 | No tests are weakened, deleted, or skipped to get green | At verdict | Yes |
| PG-F4 | No external network, no package downloads, no deployment, no software installation | Throughout the trial | Yes |
| PG-F5 | Git is not modified, committed, or initialized in the original project | Throughout the trial | Yes |

## Risks And Evidence

| Contract ID | Required | Risk or attack | Evidence | Required gate |
|---|---|---|---|---|
| PG-A1/PG-A2 | Yes | Incomplete copy or inherited runtime | Inventory before Unity | Workspace inspection |
| PG-A3 | Yes | Incompatible editor | Compare installed executable and `ProjectVersion.txt` | Version inspection |
| PG-A4 | Yes | Broken baseline or missing packages | Real XML from Unity Test Framework | EditMode batchmode |
| PG-A5 | Yes | Speculative finding | Red test at baseline, green at the end | Focused test plus EditMode suite |
| PG-I1 | Yes | Accidental change to uncommitted work | Recompute the three fingerprints | Origin hashes |
| PG-I2 | Yes | Rule moved into Unity or an external dependency | asmdef, diff, and compilation | EditMode suite |
| PG-N1/PG-N2 | Yes | Non-auditable report | Report review | Independent review |
| PG-F1/PG-F2 | Yes | Unity or the trial regenerates configuration | Diff of the copy against the origin | Diff inventory |
| PG-F3 | Yes | Test tampering | Test review and count | Full suite |
| PG-F4/PG-F5 | Yes | External effect or altered origin | Command log and fingerprints | Precheck/postcheck |

## Ambiguities

- `Library` and `Logs` may be generated after baseline. PG-A2 measures only the
  initial copy; these artifacts are removed when the trial closes.
- To avoid downloads, the copy may reuse the origin's `Library` after PG-A2 has
  been shown. That cache is disposable local data, not code or user data.
- Loopback sockets and IPC that Unity uses between its own processes do not
  count as external network under PG-F4.
- The origin project is already staged and modified without commits. PG-I1
  requires preserving exactly that state, not turning it into a clean worktree.

## Rollback

- Not applicable to the origin: only the copy is edited. A failed change is
  kept as evidence or fixed forward; the origin is never rewritten.

Conditions lock before BUILD. Any later change requires explicit user
authorization.
