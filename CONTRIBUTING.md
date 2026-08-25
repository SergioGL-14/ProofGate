# Contributing

## Before Opening A Change

- Keep the portable skill independent from host-specific configuration.
- Prefer the smallest change that improves the documented contract.
- Do not add a runner, adapter, policy format, or dependency without a concrete
  use case and a testable contract.
- Do not include local paths, credentials, private repository names, or
  conversational work logs in committed documentation.

## Validation

Run:

```bash
python -m unittest discover -s tests -v
```

Review the complete diff and run `git diff --check` before submitting a change.
Documentation changes must keep links and examples accurate.

## Evaluation Changes

Fixtures must remain deterministic and portable across supported Python
versions. Do not weaken visible tests, reference checks, thresholds, or
protected-file rules to make an evaluation pass.
