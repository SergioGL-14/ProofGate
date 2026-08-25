# Security

ProofGate is a documentation and instruction package. It does not receive
credentials, execute commands, or provide a network service by itself.

## Reporting A Vulnerability

Do not publish secrets or exploit details in a public issue. Use the repository
host's private security reporting channel when one is available. If no private
channel exists, contact the maintainers through the address published by the
repository host and include only the information needed to reproduce the issue.

## Documentation Rules

- Never commit credentials, tokens, private keys, or sensitive local paths.
- Treat evaluation workspaces and external command output as untrusted input.
- Do not describe public reference fixtures as hidden security controls.
- Keep destructive or privileged operations behind explicit authorization and
  document their rollback and post-check requirements.
