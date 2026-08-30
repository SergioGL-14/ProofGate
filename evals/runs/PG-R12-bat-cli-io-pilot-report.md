# PG-R12 - bat CLI/IO boundary pilot report

`PROOFGATE BLOCKED`

The pilot completed its baseline and boundary checks, but did not identify a
new, bounded defect with a stable contract that would justify changing the
subject repository.

## Subject and reproducibility

- Repository: `sharkdp/bat`
- Revision: `b671e53c2cd0177beb357cf6cb997ee4215c7155`
- Sandbox: disposable Docker container `rust:1.88-bookworm`
- Toolchain: `rustc 1.88.0 (6b00bc388 2025-06-23)` and Cargo 1.88.0
- Subject checkout was clean before and after the checks.
- The ProofGate repository and the subject repository were kept separate.

## Lifecycle evidence

### SCAN / CONTRACT

The selected boundary was the real `bat` CLI file and stdin path. The
contract was to distinguish successful input, empty input, invalid paths, and
directories while preserving useful exit status and stderr context.

### THREAT / TEST DESIGN

The main risks were conflating empty and invalid input, losing the failing
path in the error, and obtaining a false result from a host-mounted checkout.
The final run used a fresh Linux checkout inside the container and real CLI
invocations, not mocks.

### BUILD / GAUNTLET

All baseline gates passed at the pinned revision:

| Command | Result |
|---|---|
| `cargo fmt --check` | exit 0 |
| `cargo build --locked` | exit 0 |
| `cargo clippy --locked --all-targets --all-features` | exit 0 |
| `cargo test --locked` | exit 0; 255 integration tests passed, with the remaining unit, snapshot, and doctests also passing |

### ADVERSARY

The real CLI checks produced the following results:

| Input | Result |
|---|---|
| Existing text file | exit 0 and expected content on stdout |
| Missing file | exit 1 and the path plus OS error on stderr |
| Directory | rejected with an explicit “is a directory” error |
| Empty file | exit 0 and no fabricated content |

An initial run against a Windows-mounted copy failed integration tests because
shell fixtures retained CRLF line endings (`bash\r`). This was classified as a
host-mount artifact, discarded from the verdict, and retested from a clean
Linux checkout.

### VERDICT

`BLOCKED`: the subject is healthy at the pinned revision and the tested
contract is already covered by the implementation and tests. Existing nearby
history was also checked: the cache-help report was fixed by the subject, and
the ANSI/pager behavior was already tracked and resolved in earlier upstream
work. No new issue or pull request should be opened from this pilot.

## Limitations

Docker provided a Linux environment only. It does not validate native macOS
behavior on this Windows host; that requires a macOS runner or physical Mac.
No external repository files were changed, and no external GitHub action was
performed.
