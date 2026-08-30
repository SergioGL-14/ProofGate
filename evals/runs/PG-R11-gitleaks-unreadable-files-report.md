# PG-R11 - Gitleaks unreadable files

`PROOFGATE: FAIL`

Intensity: `ultra`
Profile: `standard`
Operation: `build`

## Subject

- Repository: [gitleaks/gitleaks](https://github.com/gitleaks/gitleaks)
- Base revision: `b58d3f102cf3a2c84cb7f923d05c25c9b1aed84b`
- Candidate revision: `d86cc86`
- Language and gates: Go, `go test`, `go vet`, `go build`, and `gofmt`
- Local copies only; the subject checkout was not modified.

## Task

Validate the reported Gitleaks behavior:
an unreadable file can be skipped while the scan reports `no leaks found` and
exits successfully. The required behavior is that incomplete scanning is
observable as a partial scan and cannot become a false `PASS`.

## Scan

- The subject is actively maintained and has an open fix proposal for this
  issue.
- The base implementation returns `nil` after `os.Open` fails in
  `sources/files.go`, so the existing partial-scan summary cannot be reached
  from that path.
- The candidate reuses the existing partial-scan branch, counts unreadable
  files, joins that error with any walk error, and adds unit plus end-to-end
  coverage.

## Contract

- `PG-A1`: a scan that cannot open a file returns an error indicating an
  incomplete scan.
- `PG-A2`: findings from readable sibling files remain available when another
  file cannot be opened.
- `PG-I1`: a scan with no unreadable files preserves its existing result.
- `PG-F1`: an unreadable file cannot produce an indistinguishable clean exit
  with code `0`.
- `PG-N1`: the behavior remains portable across supported environments, with
  permission-specific checks skipped where the host cannot model POSIX
  permissions.

## Evidence

| Gate | Revision | Command | Exit | Result |
|---|---|---|---:|---|
| Base tests | `b58d3f1` | `go test ./...` with `CGO_ENABLED=0` | 0 | PASS |
| Candidate tests | `d86cc86` | `go test ./...` with `CGO_ENABLED=0` | 0 | PASS |
| Candidate focused helper | `d86cc86` | `go test -v ./sources ./detect -run 'Unreadable'` | 0 | PASS; helper tests pass, permission E2E skipped on Windows |
| Base vet | `b58d3f1` | `go vet ./...` | 1 | BLOCKED by pre-existing context-cancel warnings |
| Candidate vet | `d86cc86` | `go vet ./...` | 1 | BLOCKED by the same pre-existing warnings |
| Candidate build | `d86cc86` | `go build .` with `CGO_ENABLED=0` | 0 | PASS |
| Candidate format | `d86cc86` | `gofmt -l` on changed files | 0 | FAIL; non-empty output listed all 3 changed files |

## Change assessment

- The candidate is a narrow 3-file change: unreadable-file accounting,
  portable helper tests, and a permission-based integration regression.
- The candidate preserves readable findings and existing walk errors.
- The end-to-end permission denial test is explicitly skipped on Windows,
  matching the project's portability rationale; this run therefore did not
  execute the core acceptance path on the current host.
- The candidate was evaluated only as a reference implementation; the report
  makes no claim beyond the recorded evidence.

## Verdict rationale

The candidate has strong source-level and unit-test evidence, and its normal
test/build gates pass. However, the format gate fails because `gofmt -l`
reports all three changed files. The mandatory end-to-end acceptance test also
cannot execute on Windows because `chmod 0000` does not reliably deny the
owning user, and the base and candidate share a failing `go vet` gate. The
result is `FAIL` for the concrete formatting defect, with the core acceptance
path additionally `BLOCKED` pending an environment with enforceable file
permissions or an independently portable permission-failure fixture.

## Limitations

- No Linux or macOS execution was available for the permission-denial test.
- `go test -race` was not run because the host lacks a C compiler for cgo.
- The candidate PR was evaluated as an external reference; the ProofGate
  repository itself was not modified beyond this report and its index entry.

## Closure status

PG-R11 is closed as a Windows-limited evaluation. Its core acceptance path is
`BLOCKED`, not `PASS`, because this project does not have a host capable of
executing the POSIX permission-denial test. No further local Windows work can
convert that missing evidence into proof of Gitleaks' real file-opening path.

If the candidate is ever re-evaluated on a suitable host, the following
closure gates apply to the pinned revision:

- `gofmt -l` returns no changed files;
- `go test ./...` passes;
- `go build .` passes;
- `go vet ./...` is either clean or its baseline-equivalent warnings are
  explicitly dispositioned by the evaluator;
- the permission-denial end-to-end test executes, rather than being skipped,
  on a host with enforceable unreadable-file semantics;
- the final report records the host, exact revision, commands, exit codes,
  changed paths, and any skipped gates.

The portable evaluator cannot substitute for the last gate: a deterministic
fixture can test ProofGate's handling of incomplete evidence, but cannot prove
that Gitleaks' real file-opening path behaves correctly. The final disposition
therefore remains `FAIL` for the observed formatting defect and `BLOCKED` for
the unavailable core acceptance path. This is the terminal local verdict for
PG-R11 unless the available host capabilities change.
