# Evaluation

## Objective

Evaluation measures whether ProofGate lets an agent produce a change that is
supported by executable evidence rather than exhaustive manual review. The
subject repository is a test environment for ProofGate, not the product being
developed.

An evaluation must test whether the agent recognizes inadequate evidence. A
project without tests should cause ProofGate to design and add the smallest
real harness needed for the contract; a green but insensitive suite should be
strengthened with evidence capable of detecting the plausible defect.

Compare the same task with and without ProofGate when the experiment permits.
Keep the repository revision, task, permissions, available tools, commands,
exit codes, final diff, verdict, interventions, and limitations. Record time or
token measurements only when the host exposes them.

## Public Fixtures

The fixtures under `evals/fixtures/` contain prepared projects, visible tests,
and reference checks. They are public and reproducible. They are not suitable
as a secrecy mechanism because anyone with repository access can inspect the
reference checks.

The fixture set covers boundary handling, untrusted paths, public contracts,
concurrency, migrations, secret leakage, operational safeguards, ambiguity,
real integration paths, and test manipulation.

External subjects may use any language, framework, or host. Prefer medium-sized real
repositories with an existing test gate and a bounded task. Do not select a
subject only because it has an open defect report.

ProofGate is designed for Windows and Linux. Windows is the reference platform
for the repository checks, and Linux validation is supported through a native
Linux host or an isolated Docker environment. macOS is outside the current
scope and has not been implemented or validated. A subject or contract that
requires native macOS filesystem, permissions, compiler, or runtime semantics
must therefore be reported as `BLOCKED` until a macOS runner or Mac is
available. This is a documented scope boundary, not a reason to infer a
successful result.

## Running The Repository Checks

Run the package contract tests from the repository root:

```bash
python -m unittest discover -s tests -v
```

The tests run the visible fixture suites and confirm that the reference checks
reject each prepared baseline. They also reproduce the preserved Phase 2
submissions.

## Evaluation Runner

The runner automates evaluator-side mechanics for the public fixtures:

```bash
python evals/runner.py prepare <fixture> <workspace>
python evals/runner.py inventory <workspace>
python evals/runner.py evaluate <fixture> <workspace>
```

`prepare` copies only the fixture project into a new workspace. `inventory`
prints deterministic per-file hashes and their aggregate. `evaluate` records
the changed paths and executes visible tests followed by the public reference
check in separate processes.

The runner exits 0 for `PASS`, 1 for `FAIL`, and 2 for `BLOCKED`. PG-E08 remains
`BLOCKED` even when both automated gates pass because its ask-before-edit
checkpoint requires separately recorded human evidence. The runner does not
launch agents, parse conversations, or provide a secrecy boundary.

Built-in fixtures use the repository's `unittest` convention. A fixture for
another ecosystem can declare shell-free command arrays and completion evidence
in `runner.toml`:

```toml
[runner]
visible = ["node", "--test", "visible.test.js"]
reference = ["node", "--test", "oracle/reference.test.js"]
visible_completion = "(?P<evidence>tests [1-9]\\d*.*fail 0)"
reference_completion = "(?P<evidence>tests [1-9]\\d*.*fail 0)"
visible_completion_stream = "stdout"
reference_completion_stream = "stdout"
manual_evidence_required = false
```

The fixture selector may be a packaged fixture ID or an absolute fixture path.
Commands are requested with `shell=False` and recorded as JSON argument arrays.
Platform script launchers such as Windows `.cmd` files may still involve the
platform command processor. Completion expressions are evaluator-owned
regular expressions over `stdout`, `stderr`, or their combined output. Each
expression must capture non-empty completion text in a named `evidence` group;
exit code 0 alone is insufficient. Built-in `unittest` gates also require a
random evaluator wrapper attestation emitted only after a non-empty suite
returns successfully.

Gate processes receive an allowlisted environment and run against disposable
copies, but this is not an operating-system sandbox. Evaluate only trusted
local subjects unless the host provides filesystem, process, and network
isolation. Gate output is evidence and is printed verbatim; it must not contain
secrets. Command argument vectors are also recorded verbatim and must never
contain credentials.

The runner compares file paths and bytes before and after each disposable gate.
It does not attest permissions, executable bits, empty directories, or other
filesystem metadata. Arbitrary code running without a host sandbox may still
inspect the host or deliberately imitate framework output; use host-level
filesystem, process, and network isolation when hostile-code resistance is part
of the contract.

## Interpreting Historical Evidence

The reports under `evals/runs/` are sanitized summaries of validation runs. They
record scope, executed evidence, and limitations. They are not a product
roadmap, a user activity log, or proof that every possible host integration is
complete.

External validation must record the repository revision, exact task, allowed
tools, commands and exit codes, final diff, verdict, interventions, and known
limitations. A missing mandatory record is `BLOCKED`, not an inferred pass.

PG-R11 demonstrates why the distinction matters in practice. Against Gitleaks,
the candidate's normal tests and build passed, while `gofmt` failed and the
permission-denial end-to-end test was skipped on Windows. The report records
`FAIL` for the concrete formatting defect and separately records the platform
limitation as `BLOCKED`; neither condition is silently converted into `PASS`.

## Known Limitations

- The public fixtures are not an unseen benchmark.
- The evaluation runner does not orchestrate base-versus-ProofGate agent runs.
- Host timing and token measurements depend on the host and may be unavailable.
- Host filesystem access is not an isolation boundary unless the host provides
  one.
- Current evaluations still depend on the agent and host to execute and report
  evidence honestly; no independent runner enforces every claim yet.
- Permission-sensitive contracts may require a host with stronger filesystem
  semantics than the evaluation host. A skipped platform test is missing
  evidence, not evidence of success.

## Preflight and risk controls

Before a real-repository run, record whether the host can provide each
required capability: disposable workspace creation and cleanup, enforceable
file permissions, loopback-only networking, the project's toolchain, and any
required compiler or browser runtime. If a capability is unavailable, mark
the affected contract `BLOCKED` before interpreting green tests.

Keep external subjects in disposable local copies. Do not place credentials in
command arguments, environment variables captured by reports, fixture output,
or test data. Prefer loopback services and network-disabled execution for
boundary tests. Treat public reference checks as regression material, never
as secrecy or isolation boundaries.

Every pilot report must separate three states when they coexist: an
implementation `FAIL`, an unavailable evidence path `BLOCKED`, and a passing
gate. This is required for cases like PG-R11, where unit tests passed while
formatting failed and the decisive permission path was skipped.

An unavailable host capability may be a terminal limitation for the local
evaluation. Close the run with an explicit bounded verdict and record what
future capability would be needed; do not keep the roadmap blocked behind an
operating system the project cannot access.
