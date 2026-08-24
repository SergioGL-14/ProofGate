# ProofGate Commands

These portable command prompts bind a host command to one ProofGate operation.
They require the `proofgate` skill to be available to the host.

| Command | Operation | Editing |
|---|---|---|
| `/proofgate-plan` | `plan` | No |
| `/proofgate-build` | `build` | Yes, within authorization |
| `/proofgate-verify` | `verify` | No |
| `/proofgate-audit` | `audit` | No |

For OpenCode, copy the four `proofgate-*.md` files into
`.opencode/command/` for one project or `~/.config/opencode/command/` for the
current user. Do not copy this README into a command directory. Hosts that do
not support command prompts can use the equivalent operation and arguments in
natural language.

Arguments may select an intensity (`lite`, `full`, `ultra`) and the `infra`
profile. If omitted, the skill determines the minimum required intensity.
