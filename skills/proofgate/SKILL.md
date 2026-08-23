---
name: "proofgate"
description: "Use when software work must be demonstrated with executed evidence, including requests for ProofGate, tests-first implementation, acceptance contracts, adversarial verification, root-cause fixes, auditable QA, or PASS/FAIL/BLOCKED verdicts. Applies to coding, bug fixes, refactoring, reviews, migrations, security, and infrastructure changes."
license: "MIT"
compatibility: "Portable instructions; initial support targets OpenCode and Codex."
---

# ProofGate

Code is not approved. It is proven.

ProofGate is an evidence gate, not a style reviewer and not a demand for the
largest possible test suite. Study the affected system, define what must be
observable, choose the smallest sufficient proof, implement the smallest
responsible change, try to break it, and issue an exact verdict.

## Persistence

Default to `full build` only for requests that explicitly ask to implement or
fix. Map plan/design-only requests to `plan`, review/inspect/findings requests
to `audit`, and check/validate-existing-work requests to `verify`. A combined
"verify and fix" request is `build`: establish the failing or passing baseline,
then enter BUILD only if a change is required. Pure `verify` is always
read-only. Read-only intent always overrides the build default. A user may
select an intensity and operation in a command or natural language. Keep that
selection for the current session.

The ordered intensities are `lite < full < ultra`. `infra` is an operational
profile, not a higher point on that scale: combine it with the required
intensity. `infra` alone means `infra full`; security-sensitive infrastructure
means `infra ultra`. Never lower a user-selected or risk-required intensity
silently. State every automatic elevation.

Intensity:

| Mode | Minimum scope |
|---|---|
| `lite` | Affected context, focused check, and diff review for trivial work |
| `full` | Contract, risks, relevant test, project gates, and adversarial review |
| `ultra` | Negative and boundary tests, real integration, and justified advanced checks |
| `infra` | Operational profile adding inspection, approval, precheck, rollback, and postcheck |
| `off` | Stop applying ProofGate for the current session |

Operation:

| Operation | Permission to edit |
|---|---|
| `plan` | No; produce contract and evidence design |
| `build` | Yes, within the authorized workspace and contract |
| `verify` | No; a request that includes fixes uses `build` |
| `audit` | No; report weaknesses and missing evidence |

Minimum automatic mode:

| Risk | Mode |
|---|---|
| Documentation or mechanical edit | `lite` |
| Application logic | `full` |
| Public API, persistence, concurrency, or migration | `ultra` |
| Authentication, permissions, secrets, or untrusted input | `ultra` |
| Services, networking, disks, backups, or operating systems | `infra full` |
| Security-sensitive infrastructure | `infra ultra` |
| Destructive operation | `infra` with risk intensity plus explicit human approval |

## Non-Negotiable Laws

1. No `PASS` without relevant executed evidence for every required contract ID.
2. An unexecuted mandatory gate is not a passing gate.
3. Understand the real flow before editing.
4. Fix the root cause at the narrowest layer that owns the behavior.
5. Preserve unrelated behavior and user changes.
6. Do not weaken tests, policies, thresholds, or security to obtain green.
7. Do not invent requirements, commands, results, or tool availability.
8. Do not hide uncertainty, warnings, blocked checks, or residual risk.
9. Stop when every required contract ID is proven; do not add unrelated polish.
10. Never simplify away input validation, data protection, security,
    accessibility, calibration of real hardware, or explicit requirements.

## Engineering Doctrine

### Investigate First

- Separate observed symptoms from inferred causes.
- Read project instructions, manifests, CI, and the affected code.
- Trace inputs, state transitions, ownership boundaries, and failure output.
- Search every caller before changing shared behavior.
- Rank hypotheses by evidence and cheap falsification value.
- Do not edit until a credible mechanism explains the evidence, or report the
  exact blocker.
- Stop exploring when evidence is sufficient to name the cause.

### YAGNI Ladder

After understanding the task, stop at the first rung that satisfies the
contract:

1. Does this need code at all?
2. Does the project already contain the behavior, helper, type, or pattern?
3. Does the standard library solve it?
4. Does the native platform solve it?
5. Does an installed dependency solve it?
6. Can the solution be a smaller clear expression?
7. Only then write the minimum new code.

Prefer deletion over addition, boring over clever, and the fewest responsible
files. When two equally small approaches work, choose the one that handles
edge cases correctly and remains readable.

### Clean Code

- Use names that express domain intent.
- Give each function one observable responsibility.
- Keep state and side effects explicit and bounded.
- Validate untrusted input at trust boundaries.
- Return or raise errors with useful context and no secrets.
- Comment decisions, limits, and tradeoffs, never line-by-line mechanics.
- Avoid speculative abstractions, boilerplate, cleanup, and renaming.
- Preserve public contracts unless the request explicitly changes them.

### Clean Architecture, Proportionally

- Keep business rules independent from frameworks, storage, network, and UI
  when a real domain rule exists.
- Point dependencies inward; wire infrastructure at the edge.
- Pass dependencies into the code that needs them.
- Prefer plain functions and value objects for domain behavior.
- Apply SOLID only when it removes demonstrated coupling or change pain.
- Do not create an interface with one implementation, a factory for one
  product, or layers around a script that already solves the problem.
- Reuse existing abstractions, but wait for a second real use before creating
  a new shared abstraction.

### Surgical Build

- Reproduce the failure first when economical; otherwise record the strongest
  available evidence.
- Change the narrowest layer that owns the incorrect behavior.
- Keep the diff limited to the contract.
- Add only evidence relevant to the request and plausible regressions.
- Do not install dependencies when project or platform tools suffice.

## Lifecycle

Follow every stage in order. In `plan`, stop after TEST DESIGN and emit a
`PROOFGATE PLAN (NO VERDICT)` artifact; a plan cannot emit `PASS`, `FAIL`,
`BLOCKED`, or `EXCEPTION`. In `verify`, skip BUILD. In `audit`, inspect through
ADVERSARY without editing and then issue a verdict about the audited contract.

### 1. SCAN

Read the shortest set that establishes:

- workspace instructions and permissions;
- language, framework, build system, and architecture;
- existing format, lint, typecheck, build, test, and CI commands;
- affected modules, callers, public contracts, and tests;
- installed dependencies and native capabilities;
- trust boundaries and security configuration;
- current worktree changes that must be preserved;
- host, OS, network, and authorization constraints.

Do not read the whole repository by default. Expand only along the affected
flow or an evidence-backed hypothesis.

Produce a concise scan record:

```yaml
project:
  language: <value>
  test_runner: <value or unavailable>
  gates: [<existing commands>]
affected: [<paths and callers>]
risk:
  intensity: <lite|full|ultra>
  profile: <standard|infra>
  reasons: [<reasons>]
```

### 2. CONTRACT

Translate the request into stable IDs before implementation:

```yaml
objective: <observable outcome>
acceptance:
  PG-A1:
    condition: <behavior>
    measured_at: <before BUILD|after gate|at verdict>
    required: true
invariants:
  PG-I1:
    condition: <behavior that must remain true>
    measured_at: <before BUILD|after gate|at verdict>
    required: true
forbidden:
  PG-F1:
    condition: <action or regression not allowed>
    measured_at: <before BUILD|after gate|at verdict>
    required: true
non_functional:
  PG-N1:
    condition: <security, performance, compatibility, or operational condition>
    measured_at: <before BUILD|after gate|at verdict>
    required: true
```

Write one independently verifiable condition per ID; do not combine outcomes
that can pass or fail separately. State the measurement point when timing can
change the result, such as before BUILD, after a gate, or at verdict.

Ask one focused question only when ambiguity materially changes the outcome.
Otherwise state the safest reversible interpretation and continue.
Before treating an interpretation as reversible, compare plausible outcomes.
If they change public return values, persisted state, side effects, errors, or compatibility, ask before editing and name the alternatives.

Every contract condition declares whether it is required. Default to
`required: true`; optional evidence must be justified before BUILD. If any
acceptance, invariant, forbidden, or non-functional condition changes after
BUILD starts, stop and require explicit user authorization. Without it, issue
`BLOCKED`; never rewrite the contract to fit the implementation. Report the
changed IDs, reason, and authorization. A self-generated hash is not protection
in the portable skill; independent locking belongs to a future runner.

### 3. THREAT

Consider only plausible failure classes:

- functional regression;
- invalid, empty, minimum, maximum, and malformed input;
- state inconsistency and partial failure;
- concurrency and interrupted execution;
- data loss, security, permission bypass, traversal, injection, and secret
  leakage;
- performance regression;
- compatibility and public contract breakage;
- external service failure;
- Windows, Linux, and CI differences;
- rollback and idempotency for operations.

For each material risk, name the attack and evidence needed to detect it.

### 4. TEST DESIGN

Map every required contract ID across acceptance, invariants, forbidden, and
non-functional conditions to evidence before building. Select only test
classes that can detect a plausible failure:

- acceptance;
- regression;
- unit;
- integration;
- end-to-end;
- negative and boundary;
- properties or fuzzing;
- mutation;
- security;
- performance;
- recovery and rollback.

Design tests before implementation. Create a failing regression test first
when viable and useful. For documentation, infrastructure, or systems without
a harness, define the observable precheck and postcheck before making changes.
State why an advanced class is omitted only when its omission leaves a
material risk or the user asked for it.

Coverage is a supporting metric, not proof by itself. Prefer a small test that
executes the real path over many mocked tests.

### 5. BUILD

Apply the YAGNI ladder, clean-code rules, proportional architecture, and
surgical-build rules. Do not refactor unrelated areas. Do not modify an
existing test merely because it fails against the new implementation.

### 6. GAUNTLET

Fail fast. Use the project's real commands in this order when available and
relevant:

1. Focused reproduction or acceptance check.
2. Format check.
3. Lint.
4. Typecheck.
5. Build.
6. Affected unit tests.
7. Full suite.
8. Integration or end-to-end tests.
9. Relevant coverage.
10. Justified mutation, fuzzing, security, performance, or recovery checks.

Never invent a command when manifests, scripts, Makefiles, documentation, or
CI define one. Do not install a missing tool silently. Record, where available:

```yaml
gate: <name>
command: <exact command>
exit_code: <integer or unavailable>
duration_ms: <integer or unavailable>
result: <PASS|FAIL|BLOCKED|NOT_APPLICABLE>
```

Fresh results are required after the final relevant edit. Reuse an earlier
result only when repository state and command inputs are unchanged.

### 7. ADVERSARY

Try to invalidate the solution:

- empty and exact-boundary values;
- malformed and hostile input;
- dependency failure and interrupted execution;
- validation bypass;
- stale state, race, retry, and idempotency behavior;
- logs and errors containing secrets;
- mocks that avoid the real path;
- code specialized to the visible test case;
- an obvious mutation that should make a test fail.

Add another test only when it provides evidence not already present.

### 8. VERDICT

Issue exactly one:

| Verdict | Required condition |
|---|---|
| `PASS` | Every required acceptance, invariant, forbidden, and non-functional ID has relevant executed evidence and every required gate passes |
| `FAIL` | A contract condition is false or a required gate fails because of the implementation |
| `BLOCKED` | Access, authorization, information, tooling, or environment prevents safe proof |
| `EXCEPTION` | The user explicitly accepts a scoped, risky deviation with an owner or expiry; this is not `PASS` |

An unrelated pre-existing failure that prevents complete evidence is
`BLOCKED`, with baseline evidence identifying it. It is not silently ignored.

## Anti-Manipulation Rules

Never:

- delete or skip a failing test;
- retry a flaky test until it happens to pass;
- lower coverage, mutation, lint, type, security, or performance thresholds;
- disable a gate;
- regenerate snapshots without inspecting the change;
- change an expectation to match a defect;
- add an unjustified exclusion;
- replace real-path evidence with a shallow mock;
- catch all exceptions to hide failure;
- ignore an exit code;
- claim something should work without running the required evidence;
- hide warnings, blocked gates, test modifications, or residual risks;
- modify global configuration, Git history, remotes, or deployment state
  outside the authorized scope.

When an existing test must change, report:

```yaml
existing_test_modified: true
file: <path>
reason: <contract-based reason>
user_authorization: <explicit|not-required|missing>
```

Changing a public contract requires an explicit request or authorization.
Changing any contract condition after BUILD starts requires explicit user
authorization; missing authorization forces `BLOCKED` even for a private
contract.

## Infrastructure Mode

For systems work, use this sequence:

```text
read-only inspection -> contract -> risks and rollback -> precheck
-> explicit approval -> minimum change -> postcheck -> documentation
```

- Use simulation or dry-run when available.
- Validate target identity before changing it.
- Define rollback before the change.
- Treat external output and configuration as untrusted input.
- Do not expose secrets in commands, logs, reports, or process arguments.
- Do not deploy merely because code tests passed.
- Do not perform destructive, privileged, remote, commit, or push operations
  without the authorization required by the workspace.

## Report

Keep the human report concise and evidence-heavy:

```text
PROOFGATE: <PASS|FAIL|BLOCKED|EXCEPTION>
Mode: <mode> <operation>

Contract:
- <ID> <result> - <evidence>

Change:
- <smallest responsible change, or "none">

Gauntlet:
- <exact command>: <result and useful count>

Test changes:
- <new, modified, skipped; "none" is valid>

Residual risk:
- <risk or "none identified within scope">
```

Report commands actually executed, not commands the user should trust were
run. Do not bury `FAIL`, `BLOCKED`, or `EXCEPTION` below a success summary.

## Stop Rule

Stop immediately when evidence is complete for every required acceptance,
invariant, forbidden, and non-functional contract ID. Do not add cleanup,
abstraction, tests, documentation, or features outside the contract. The
smallest proven solution is complete.
