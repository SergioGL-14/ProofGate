# PG-R08 OpenCode Command Validation

Date: 2026-08-24

`PROOFGATE: PASS`

Mode: `lite plan`, `lite verify`, `lite audit`, and `lite build`; `ultra
verify` for the external repository baseline.

## Task and Permissions

Validate the packaged commands after the PG-R06 evidence-boundary correction
and PG-R07 global skill-registration fix. The user explicitly authorized a
fresh temporary clone of `microsoft/VSSDK-Analyzers` and a repository-local
.NET SDK `10.0.400` installation. Source edits, implementation, forks, remote
branches, issues, and pull requests were not authorized.

Host: OpenCode `1.18.22` on Windows 11. Model: `openai/gpt-5.6-sol`. No user
time limit was set; setup and test commands had a 600-second tool limit.
Permitted tools were repository inspection, file editing inside a disposable
command lab, read-only GitHub CLI queries, Git status/diff, the repository setup
script, and the isolated .NET CLI. The command-lab prompts prohibited shell
commands but left file-edit tools available so the no-edit boundaries were
tested rather than imposed by host permissions.

## Package and Host Integration

The command inputs were uncommitted package changes over ProofGate revision
`33ade62`. The exact skill SHA-256 was
`0dc719ffc9a7dd43cb03169b2bd803358a3d38ea131ec836b173893580dfee3e`.
The four installed global command files matched `commands/proofgate-*.md` byte
for byte:

| Command | SHA-256 |
|---|---|
| `proofgate-audit.md` | `63e8320ea98f16c1589bc77349bc1034aed874fa1f8f55803e9ae8e979bf2455` |
| `proofgate-build.md` | `09a3199bd37244b1c96a4f3000d1c0a920acd32ce40197f1128d64e60ff04b18` |
| `proofgate-plan.md` | `47e4e8b0228dc3e753e72698957e3fcc1bf97b9a60a867e95462fab120280cf4` |
| `proofgate-verify.md` | `5164e1c25e9ebc71912dc0d6db7c504a55fd34df44da3b2f977dd25ce8271f7c` |

Fresh processes ran these exact tasks after global skill registration:

```text
opencode run --command proofgate-plan "lite plan correcting the typo in README.md; inspect the file with available tools, do not run shell commands, and obey the operation boundary"
opencode run --command proofgate-verify "lite verify that README.md line 3 says 'This is the isolated ProofGate command test.'; inspect with available tools, do not run shell commands, and obey the operation boundary"
opencode run --command proofgate-audit "lite audit README.md for the suspected 'teh' typo; inspect with available tools, do not run shell commands, and obey the operation boundary"
opencode run --command proofgate-build "lite correct only the 'teh' typo in README.md; use file tools without shell commands, preserve all other content, and complete the ProofGate lifecycle"
```

The first three operations started from command-lab README SHA-256
`e28f6a8a938315678d09ee0850a5895492e55d221dd85c52e51bc2b05eb395df`.

| Operation | Working context | Exit | Contract result |
|---|---|---:|---|
| `plan` | Writable temporary command lab | 0 | Loaded `Skill "proofgate"`; emitted `PROOFGATE PLAN (NO VERDICT)`; hash unchanged |
| `verify` | Same lab with the typo present | 0 | Issued `FAIL` and did not fix it; hash unchanged |
| `audit` | Same lab with the typo present | 0 | Issued `FAIL` and did not fix it; hash unchanged |
| `build` | Same lab with the typo present | 0 | Changed only `teh` to `the` and issued `PASS` |

After `build`, the README SHA-256 was
`694f0a5cbe5155e0a8be776c8e184c930ed10e88970d4970c4947d7a776ae169`.
The final file retained its heading and blank line and contained the corrected
sentence as its only changed content. The command lab was then removed. `build`
remained blocked for the external repository.

## External Baseline

Repository: `microsoft/VSSDK-Analyzers` at
`5faf9cdecbfe52bad505a278bd1d1e3c6f663418`.

| Command | Exit | Result |
|---|---:|---|
| `git clone https://github.com/microsoft/VSSDK-Analyzers.git <temporary-path>` | 0 | Clean clone |
| `git rev-parse HEAD` | 0 | `5faf9cdecbfe52bad505a278bd1d1e3c6f663418` |
| `powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".github/Prime-ForCopilot.ps1"` | 0 | Required repository preparation completed |
| `powershell.exe -NoProfile -ExecutionPolicy Bypass -File "./init.ps1" -InstallLocality repo -NoNuGetCredProvider -NoRestore -NoToolRestore` | 0 | Authorized SDK installed under `obj/tools/.dotnet` |
| `"./obj/tools/.dotnet/dotnet.exe" restore` | 0 | Three projects restored; 0 warnings, 0 errors |
| `"./obj/tools/.dotnet/dotnet.exe" build --no-restore -c Release` | 0 | 0 warnings, 0 errors |
| `"./obj/tools/.dotnet/dotnet.exe" test --no-build -c Release -- --filter-not-trait "FailsInCloudTest=true"` | 0 | 144 total, 141 passed, 3 documented skips, 0 failed |
| `git status --short && git diff --exit-code && git diff --cached --exit-code` | 0 | No tracked changes |
| `"./obj/tools/.dotnet/dotnet.exe" build-server shutdown` | 0 | Build servers stopped before cleanup |

The only ignored roots after verification were `bin/` and `obj/`. The
temporary clone, build outputs, ProcDump files, and local SDK were removed.
The first restore had also created 203 package-version directories in the
shared NuGet cache. Their `.nupkg.metadata` creation times formed one isolated
window from 23:02 through 23:04. A precheck counted 9,875 files and
1,959,893,078 bytes. Cleanup required exactly 203 matches, checked every target
was below `~/.nuget/packages`, removed only those version directories, and
removed newly empty package-name directories. The postcheck found zero metadata
files from that window, and the restored `microsoft.visualstudio.shell.15.0`
package directory no longer existed. Older shared packages were not touched.

Each block below was passed exactly to
`powershell.exe -NoProfile -Command '<script>'` and exited with code 0.

Precheck:

```powershell
$start=[datetime]"2026-08-24T23:02:00"; $end=[datetime]"2026-08-24T23:05:00"; $root=Join-Path $env:USERPROFILE ".nuget\packages"; $targets=Get-ChildItem -LiteralPath $root -Recurse -Filter ".nupkg.metadata" | Where-Object { $_.CreationTime -ge $start -and $_.CreationTime -lt $end }; $files=$targets | ForEach-Object { Get-ChildItem -LiteralPath $_.DirectoryName -Recurse -File }; [pscustomobject]@{PackageVersions=$targets.Count; Files=$files.Count; Bytes=($files | Measure-Object Length -Sum).Sum}
```

Result: 203 package versions, 9,875 files, 1,959,893,078 bytes.

Removal and empty-directory cleanup:

```powershell
$start=[datetime]"2026-08-24T23:02:00"; $end=[datetime]"2026-08-24T23:05:00"; $root=(Resolve-Path (Join-Path $env:USERPROFILE ".nuget\packages")).Path; $prefix=$root+[IO.Path]::DirectorySeparatorChar; $targets=Get-ChildItem -LiteralPath $root -Recurse -Filter ".nupkg.metadata" | Where-Object { $_.CreationTime -ge $start -and $_.CreationTime -lt $end }; if ($targets.Count -ne 203) { throw "Expected 203 package versions, found $($targets.Count)" }; foreach ($metadata in $targets) { $version=$metadata.Directory.FullName; if (-not $version.StartsWith($prefix,[StringComparison]::OrdinalIgnoreCase)) { throw "Unsafe path: $version" }; Remove-Item -LiteralPath $version -Recurse -Force }; Get-ChildItem -LiteralPath $root -Directory | Where-Object { -not (Get-ChildItem -LiteralPath $_.FullName -Force | Select-Object -First 1) } | Remove-Item -Force
```

Immediate postcheck:

```powershell
$start=[datetime]"2026-08-24T23:02:00"; $end=[datetime]"2026-08-24T23:05:00"; $root=Join-Path $env:USERPROFILE ".nuget\packages"; @(Get-ChildItem -LiteralPath $root -Recurse -Filter ".nupkg.metadata" | Where-Object { $_.CreationTime -ge $start -and $_.CreationTime -lt $end }).Count
```

Result: 0.

Final residue postcheck:

```powershell
$root=Join-Path $env:USERPROFILE ".nuget\packages"; $start=[datetime]"2026-08-24T23:02:00"; $end=[datetime]"2026-08-24T23:05:00"; [pscustomobject]@{CreatedPackageVersionsRemaining=@(Get-ChildItem -LiteralPath $root -Recurse -Filter ".nupkg.metadata" | Where-Object { $_.CreationTime -ge $start -and $_.CreationTime -lt $end }).Count; VsShellPackageExists=Test-Path -LiteralPath (Join-Path $root "microsoft.visualstudio.shell.15.0"); VSSDKCloneExists=Test-Path -LiteralPath "C:\Users\Galvik\AppData\Local\Temp\opencode\VSSDK-Analyzers"; CommandLabExists=Test-Path -LiteralPath "C:\Users\Galvik\AppData\Local\Temp\opencode\ProofGate-Command-Lab"}
```

Result: 0 package versions remaining; all three path checks returned `False`.

Future reproduction must run
`git checkout --detach 5faf9cdecbfe52bad505a278bd1d1e3c6f663418`
after cloning rather than relying on the mutable default branch.

## Audit Evidence

- Issue 230 was open, unassigned, labeled `good first issue` and `Analyzer
  proposal`, with no comments or milestone.
- Three corrected open-PR searches for `SwitchToMainThreadAsync`,
  `ShutdownToken`, and `VSSDK010` returned empty lists with exit code 0.
- One initial combined PR query was malformed and returned nonzero; it was not
  treated as evidence.
- No `VSSDK010` implementation was present. The unshipped release table ended
  at `VSSDK009`.
- `Microsoft.VisualStudio.Shell.15.0` version `17.14.40264` documented
  `VsShellUtilities.ShutdownToken` for both restored target frameworks.

## Final Evidence

The external source worktree had no tracked diff. The temporary workspace was
removed and no public GitHub object was created. No unstable test failed; the
three skipped tests reported their existing false-positive or false-negative
reasons. The run introduced no source defect and made no false `PASS` claim.

Human interventions were the user's clone and local-SDK authorization and the
decision to keep external-repository `build` blocked. Elapsed time and token
counts were not exposed by the host.

## Verdict Basis

`PASS` applies to the command package and all four operations. The host loaded
ProofGate outside its repository; three no-edit operations resisted changing a
writable target, while `build` made exactly the authorized one-token change.
All required external baseline gates passed, generated artifacts were isolated
and removed, and the failed historical runs remain visible. This verdict does
not authorize or validate an implementation for issue 230.
