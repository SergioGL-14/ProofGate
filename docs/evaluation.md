# Evaluation

## Public Fixtures

The fixtures under `evals/fixtures/` contain prepared projects, visible tests,
and reference checks. They are public and reproducible. They are not suitable
as a secrecy mechanism because anyone with repository access can inspect the
reference checks.

The fixture set covers boundary handling, untrusted paths, public contracts,
concurrency, migrations, secret leakage, operational safeguards, ambiguity,
real integration paths, and test manipulation.

## Running The Repository Checks

Run the package contract tests from the repository root:

```bash
python -m unittest discover -s tests -v
```

The tests run the visible fixture suites and confirm that the reference checks
reject each prepared baseline. They also reproduce the preserved Phase 2
submissions.

## Interpreting Historical Evidence

The reports under `evals/runs/` are sanitized summaries of validation runs. They
record scope, executed evidence, and limitations. They are not a product
roadmap, a user activity log, or proof that every possible host integration is
complete.

External validation must record the repository revision, exact task, allowed
tools, commands and exit codes, final diff, verdict, interventions, and known
limitations. A missing mandatory record is `BLOCKED`, not an inferred pass.

## Known Limitations

- The public fixtures are not an unseen benchmark.
- The repository does not include an automated benchmark runner.
- Host timing and token measurements depend on the host and may be unavailable.
- Host filesystem access is not an isolation boundary unless the host provides
  one.
