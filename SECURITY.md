# Security

ProofGate is a documentation and instruction package. It does not receive
credentials, execute commands, or provide a network service by itself.

## Reporting A Vulnerability

Do not publish secrets or exploit details in a public issue. Use
[GitHub private vulnerability reporting](https://github.com/SergioGL-14/ProofGate/security/advisories/new),
which is enabled for this repository, and include only the information needed
to reproduce the issue safely.

## Documentation Rules

- Never commit credentials, tokens, private keys, or sensitive local paths.
- Treat evaluation workspaces and external command output as untrusted input.
- Do not describe public reference fixtures as hidden security controls.
- Keep destructive or privileged operations behind explicit authorization and
  document their rollback and post-check requirements.
