# PG-R09 - Evaluation Runner Pilot

`PROOFGATE: PASS`

Intensity: `full`
Profile: `standard`
Operation: `build`
Record status: `complete`

## Subject

- Repository: `sindresorhus/yocto-queue`
- Revision: `b07eac0`
- Language and gates: JavaScript, `npm test`, and `node:test`
- Scope: local evaluator fixture; the subject checkout remained unchanged.

The prepared defect changed queue iteration to stop on a falsy value. This was
an evaluator mutation, not a defect observed in the upstream revision.

## Exact Task And Limits

```text
Fix queue iteration so every enqueued value is yielded in FIFO order, including
JavaScript falsy values. Preserve the public API and add regression evidence.
```

- Allowed tools: local file inspection and edits, Node.js, npm for the upstream
  baseline, and the ProofGate evaluator runner.
- Network: allowed only for the explicitly authorized temporary development
  dependency installation.
- Forbidden: changes to the subject checkout or its history, and changes
  outside temporary subject and evaluator-fixture copies.
- Isolation: disposable runner copies and an allowlisted environment; no claim
  of operating-system sandboxing.

## Contract

- PG-A1: the runner supports fixture-declared argument arrays requested with
  `shell=False`.
- PG-A2: visible success plus reference failure produces `FAIL`.
- PG-A3: visible and reference success with completion evidence produces
  `PASS`.
- PG-I1: the upstream checkout remains unchanged.
- PG-F1: missing or mismatched completion evidence cannot produce `PASS`.

## Evidence

- Upstream baseline: `npm test` exited 0 with 7 AVA tests passing and the TSD
  gate complete.
- Prepared baseline visible gate: `node --test visible.test.js` exited 0 with
  1 test passing.
- Prepared baseline reference gate: `node --test oracle/reference.test.js`
  exited 1 because iteration returned no values when the first item was `0`.
- Runner baseline verdict: `FAIL`.
- Regression-first gate: the new falsy-value test exited 1 before the fix.
- Final visible gate: exited 0 with 2 tests passing.
- Final reference gate: exited 0 with 1 test passing.
- Final runner verdict: `PASS`.
- Final changed paths: `index.js` and `visible.test.js`.

## Final Diff

```diff
diff --git a/index.js b/index.js
@@
-		while (current?.value) {
+		while (current) {

diff --git a/visible.test.js b/visible.test.js
@@
+test('queue iteration preserves falsy values', () => {
+	const queue = new Queue();
+	for (const value of [0, false, '', undefined, null, 'last']) {
+		queue.enqueue(value);
+	}
+	assert.deepEqual([...queue], [0, false, '', undefined, null, 'last']);
+});
```

The first Node completion expression did not match Node's actual output, so the
runner returned `BLOCKED` despite both gates exiting 0. Correcting the
evaluator-owned expression produced `PASS`; no test, threshold, or subject code
was weakened to obtain it.

## Run Record

- Model: OpenAI coding agent; exact model identifier omitted from the public
  evidence package.
- Host: OpenCode on Windows.
- Time limit: no fixed agent limit; evaluator commands used 120-second gate
  timeouts.
- Defects found: one prepared falsy-value iteration defect.
- Defects introduced: none detected by final visible and reference gates.
- False `PASS`: none; one completion mismatch correctly produced `BLOCKED`.
- Unstable tests: none observed across the recorded reruns.
- Human interventions: dependency installation authorization and selection of
  the external subject.
- Elapsed time and tokens: unavailable as a complete host measurement.

## Dependency Observation

Development dependencies were installed in the temporary checkout with
scripts disabled. Installation reported five moderate development dependency
advisories. `npm audit --omit=dev --json` reported no production dependency
vulnerabilities. No automated remediation was run.

## Limitations

- The runner evaluated prepared workspaces; it did not launch or compare agent
  conversations.
- Completion expressions are evaluator-owned evidence but are not a security
  boundary against code running outside a sandbox.
- A hostile subject running without host isolation can still imitate framework
  output or inspect accessible host files.
- This pilot proves language-independent gate execution for one Node project,
  not universal host compatibility.
