# Usage

## Select An Operation

Use one operation for each request:

```text
ProofGate full plan <task>
ProofGate full build <task>
ProofGate full verify <target>
ProofGate full audit <target>
```

The host may expose these operations as commands. The packaged OpenCode
commands are `/proofgate-plan`, `/proofgate-build`, `/proofgate-verify`, and
`/proofgate-audit`.

## Intensity And Profile

| Selection | Use |
|---|---|
| `lite` | Documentation or mechanical changes |
| `full` | Normal application work |
| `ultra` | Public contracts, persistence, concurrency, migrations, or security |
| `infra` | Operational work involving services, permissions, systems, or backups |
| `off` | Disable ProofGate for the current session |

`infra` is a profile, not an intensity. Used alone, it selects `infra full`.
Use it with `ultra` for security-sensitive operational work.

## Verdicts

- `PASS`: every required condition has relevant executed evidence.
- `FAIL`: a required condition is false or an implementation gate fails.
- `BLOCKED`: required access, information, tooling, or environment is missing.
- `EXCEPTION`: an explicitly authorized risk is accepted with an owner and
  review date.

Plans use `PROOFGATE PLAN (NO VERDICT)` and never issue a final verdict.

## Host Installation

For OpenCode:

1. Add the repository's `skills/` directory to the host's `skills.paths`.
2. Copy the four `proofgate-*.md` files to `.opencode/command/` or the global
   command directory.
3. Start a new session and verify that the `proofgate` skill is available.

Minimal `opencode.json` configuration:

```json
{
  "skills": {
    "paths": ["/path/to/ProofGate/skills"]
  }
}
```

Replace the example path with the cloned repository's `skills/` directory. The
command files are installed separately because the host does not load commands
from `skills.paths` automatically.

No command should silently install dependencies or change global configuration.
