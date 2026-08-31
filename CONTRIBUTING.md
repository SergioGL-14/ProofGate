# Contributing

## Before Opening A Change

- Keep the portable skill independent from host-specific configuration.
- Prefer the smallest change that improves the documented contract.
- Do not add a runner, adapter, policy format, or dependency without a concrete
  use case and a testable contract.
- Do not include local paths, credentials, private repository names, or
  conversational work logs in committed documentation.
- Keep the purpose visible: reduce exhaustive review of generated code through
  executable evidence, restrictions, and adversarial checks.

## Validation

Run:

```bash
python -m unittest discover -s tests -v
```

Review the complete diff and run `git diff --check` before submitting a change.
Documentation changes must keep links and examples accurate.

Pull requests should use the repository template and keep the final diff
limited to one contract. Bug reports must include a minimal reproduction or
state why one is unavailable.

## External Evaluation Subjects

Use external repositories as experimental subjects when testing ProofGate. The
subject may use any language or host. Keep it separate from this repository,
record the exact revision and evidence, and do not modify the subject as part
of the evaluation.

## Evaluation Changes

Fixtures must remain deterministic and portable across supported Python
versions. Do not weaken visible tests, reference checks, thresholds, or
protected-file rules to make an evaluation pass.

New real-repository reports must satisfy the recording fields in
`evals/README.md`. Historical summaries may be retained, but must be labelled
as legacy and must not support reproducibility or effectiveness claims.

## Releases

- Use semantic versioning and explain any intentionally skipped version.
- Create annotated tags for future releases; do not rewrite published tags.
- Publish from a clean `main` commit whose required CI checks pass.
- Keep release notes and `CHANGELOG.md` aligned with the tagged tree.
