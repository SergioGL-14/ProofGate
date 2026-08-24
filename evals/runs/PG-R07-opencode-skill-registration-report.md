# PG-R07 OpenCode Skill Registration

Date: 2026-08-24

`PROOFGATE: FAIL`

Mode: `lite plan`

## Task

Confirm that the globally registered `/proofgate-plan` command dispatches the
ProofGate skill and preserves the no-edit, no-verdict boundary.

Host: OpenCode `1.18.22` on Windows 11. Model: `openai/gpt-5.6-sol`. No user
time limit was set; each process had a 600-second tool limit. Read-only file
tools were permitted. Editing, installation, and public activity were not.

## Evidence

The command prompt loaded, but the host returned:

```text
Skill "proofgate" not found
```

The available global skill list did not include ProofGate. A second attempt
could read `skills/proofgate/SKILL.md` only because its working directory was
the ProofGate repository; this fallback would not work in another project.

Both `opencode run --command proofgate-plan ...` processes exited with code 0,
which does not correct the missing skill registration. The first attempt also
auto-rejected requested shell permissions and did not produce the required
final plan artifact. No edit tool or external write was used.

## Verdict Basis

The command file alone was not a working global integration. A command that
requires an unavailable skill cannot satisfy its contract outside this
repository. The fix was to add this repository's `skills/` directory to the
global OpenCode `skills.paths`; that fix is evaluated only in PG-R08.

Elapsed time and token counts were not exposed by the host. No project defect
was introduced, and no `PASS` was claimed.
