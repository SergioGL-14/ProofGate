# PG-R02 - State Transition Regression

`PROOFGATE: PASS`

Intensity: `ultra`
Profile: `standard`
Operation: `build`
Record status: `legacy summary`

This run predates the current recording contract. Its missing subject,
revision, commands, and session metadata were not retained and are not
reconstructed. It is project history, not reproducible effectiveness evidence.

## Scope

The run used a disposable copy of a stateful application. A confidence value
could reach zero without ending the session, although the domain contract
defined that state as terminal.

## Evidence

- The new regression failed against the baseline.
- The minimal domain change ended the session with the correct reason.
- Adversarial review caught and prevented a later transition from overwriting
  an earlier terminal reason.
- The final editor test suite passed without changing project configuration.

## Limits

The run covered one state transition. Other domain, UI, and persistence
findings were outside scope.
