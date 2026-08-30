# PG-R12 - bat CLI/IO boundary pilot plan

`PROOFGATE PLAN (NO VERDICT)`

This is a proposed evaluation plan for a medium-sized public repository. It is
not evidence that the pilot has run.

## Subject

- Repository: `sharkdp/bat`
- Local subject revision: record the exact revision immediately before the
  first base run
- Language and gates: Rust, `cargo test`, `cargo fmt --check`, `cargo clippy`,
  and the project's build command where the selected path requires it
- Candidate area: one narrowly scoped CLI, filesystem, or rendering boundary
  in `src/`, selected only after baseline inspection identifies a concrete
  defect. The subject must be large enough to have real project gates and
  caller context, but small enough for a bounded local experiment.

A pinned local checkout is available for preparation. The pilot must use a
fresh disposable copy for every run and must not modify the source checkout.

## Contract

- `PG-A1`: the selected CLI or IO path produces the documented result for a
  successful invocation.
- `PG-A2`: the selected failure boundary preserves the documented exit status,
  stderr, and error context.
- `PG-I1`: valid paths, invalid paths, and empty input remain distinguishable.
- `PG-F1`: a visible green suite cannot hide a broken real adapter path behind
  a mock-only or snapshot-only test.
- `PG-N1`: tests do not contact external services, print credentials, or rely
  on host-global configuration.

If baseline inspection finds no bounded defect with a stable contract, stop
the pilot and record `BLOCKED`; do not invent a task merely to produce a run.

## Threats and evidence design

| Risk | Required evidence |
|---|---|
| Mock bypasses the CLI/IO boundary | Real temporary files and subprocess or project-standard integration boundary |
| Error metadata is lost | Assertions over exit status, stderr, and structured error context |
| Empty and invalid input are conflated | Separate deterministic boundary tests |
| Test reaches the network | Loopback-only endpoint and network-disabled execution where available |
| Agent changes unrelated API or fixtures | Baseline inventory, changed-path report, and protected-file check |
| Green command is not a completed suite | Cargo test completion evidence plus exit code |

## Run protocol

1. Record revision, Rust toolchain, Cargo version, available scripts, and
   dependency state.
2. Run the clean baseline gates before exposing the task to either agent.
3. Create separate fresh copies and separate conversations for base and
   ProofGate; provide only the task and project workspace.
4. Run focused tests, `cargo fmt --check`, `cargo clippy`, the relevant build,
   the full Cargo test suite, and the adversarial/reference checks in that
   order.
5. Compare inventories and changed paths before and after every gate.
6. Record elapsed time, tokens when available, interventions, exact commands,
   exit codes, diff, verdict, and limitations.
7. Delete disposable copies only after the report is complete.

## Exit criteria

The pilot is useful only if the ProofGate run is no worse than baseline,
detects any prepared defect, and records `BLOCKED` instead of inferring
success when baseline, toolchain, or a real CLI/IO boundary is unavailable. A
the result is incomplete.
