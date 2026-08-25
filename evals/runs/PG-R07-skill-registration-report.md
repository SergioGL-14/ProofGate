# PG-R07 - Skill Registration Validation

`PROOFGATE: FAIL`

Intensity: `lite`
Profile: `standard`
Operation: `plan`

## Finding

The command prompt was available to the host, but the `proofgate` skill was
not registered in the host's global skill paths. A command that cannot load its
required skill is not a working integration outside the repository.

## Evidence

- The command loaded but returned a missing-skill error.
- No project file or external resource was changed.
- The command did not produce the required plan artifact.

## Follow-up

The host skill path was configured before the subsequent command validation.
