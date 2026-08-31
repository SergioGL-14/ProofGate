# PG-R12 - bat CLI/IO Boundary Audit

`PROOFGATE: PASS`

Intensity: `full`
Profile: `standard`
Operation: `audit`
Record status: `bounded`

## Subject

- Repository: [sharkdp/bat](https://github.com/sharkdp/bat)
- Revision: [`b671e53c2cd0177beb357cf6cb997ee4215c7155`](https://github.com/sharkdp/bat/commit/b671e53c2cd0177beb357cf6cb997ee4215c7155)
- Sandbox: disposable Docker container `rust:1.88-bookworm`
- Toolchain: `rustc 1.88.0 (6b00bc388 2025-06-23)` and Cargo 1.88.0
- Subject checkout: clean before and after the audit.

## Exact Task And Limits

Audit the real `bat` CLI file and standard-input boundary for a bounded defect
that could justify a contribution. Distinguish valid, empty, missing, and
directory inputs while preserving useful exit status and stderr context. Do
not modify the subject or open an upstream issue or pull request unless a new,
reproducible defect survives the project gates and adversarial checks.

- Allowed tools: local source and history inspection, Docker, Cargo, and real
  CLI invocations in the disposable Linux container.
- Network: used to obtain the public subject and container dependencies; no
  credentials were required or recorded.
- Time limit, elapsed time, and token count: unavailable from the host.
- Human interventions: selection of `bat` and the CLI/IO boundary.

## Contract

| ID | Required | Result | Evidence |
|---|---|---|---|
| PG-A1 | Yes | `PASS` | A valid text file exits 0 and emits its expected content. |
| PG-A2 | Yes | `PASS` | An empty file exits 0 without fabricated content. |
| PG-A3 | Yes | `PASS` | A missing path exits 1 and stderr contains the path and OS error. |
| PG-A4 | Yes | `PASS` | A directory is rejected with an explicit directory error. |
| PG-I1 | Yes | `PASS` | Format, build, lint, full tests, and the tracked checkout remain clean. |
| PG-F1 | Yes | `PASS` | No defect, patch, issue, or pull request is invented from passing evidence. |

## Threat And Test Design

The material risks were conflating empty and invalid input, losing the failing
path in the error, and accepting a false result from a Windows-mounted checkout.
The final checks used a fresh Linux checkout inside the container and real CLI
invocations rather than mocks.

## Change

- None. The operation was an audit and the selected behavior already satisfied
  its contract.

## Gauntlet

| Gate | Command | Exit | Result |
|---|---|---:|---|
| Format | `cargo fmt --check` | 0 | `PASS` |
| Build | `cargo build --locked` | 0 | `PASS` |
| Lint | `cargo clippy --locked --all-targets --all-features` | 0 | `PASS` |
| Full suite | `cargo test --locked` | 0 | `PASS`; 255 integration tests plus unit, snapshot, and doctests |
| Existing text file | real `bat` CLI invocation | 0 | Expected content on stdout |
| Missing file | real `bat` CLI invocation | 1 | Path and OS error on stderr |
| Directory | real `bat` CLI invocation | nonzero | Explicit “is a directory” error |
| Empty file | real `bat` CLI invocation | 0 | No fabricated content |

## Adversarial Record

An initial run against a Windows-mounted copy failed integration tests because
shell fixtures retained CRLF line endings (`bash\r`). That result measured the
host mount, not the pinned Linux checkout. It was excluded with an explicit
reason and the entire relevant gate set was rerun from a clean checkout inside
the Linux container.

Nearby upstream history was inspected. The cache-help report was already fixed,
and the ANSI/pager behavior was already tracked and resolved. No new bounded
defect remained.

## Test Changes

- None.

## Run Record

- Defects found: none within the selected boundary.
- Defects introduced: none; the subject was not modified.
- Final diff: none.
- False `PASS`: none identified.
- Unstable tests: none after removing the documented host-mount artifact.
- External actions: no issue, pull request, commit, or push was created.

## Limitations

- Docker proved the selected Linux behavior only. Native macOS behavior remains
  outside the contract and requires a macOS runner or physical Mac.
- The exact CLI argument vectors, durations, and complete session transcript
  were not retained, so this report is bounded rather than complete.
- Passing this bounded audit does not claim that `bat` has no defects outside
  the selected CLI/IO path.

## Verdict Basis

Every required audit condition has executed evidence, all project gates pass,
the subject remains unchanged, and adversarial inspection found no defensible
contribution task. A no-change `PASS` is therefore correct; absence of a defect
is not an environmental or authorization `BLOCKED` condition.
