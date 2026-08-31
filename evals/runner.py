"""Prepare and evaluate ProofGate fixture workspaces."""

from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import tomllib


FIXTURES = Path(__file__).resolve().parent / "fixtures"
UNITTEST_COMPLETION = r"(?P<evidence>PROOFGATE_UNITTEST_COMPLETE:[a-f0-9]+)"


@dataclass(frozen=True)
class RunnerConfig:
    """Commands and completion evidence declared by an evaluation fixture."""

    visible: list[str]
    reference: list[str]
    visible_completion: str
    reference_completion: str
    visible_completion_stream: str = "combined"
    reference_completion_stream: str = "combined"
    manual_evidence_required: bool = False
    trusted_unittest: bool = False


def resolve_fixture(selector: str) -> Path:
    """Return the uniquely selected fixture or raise a user-facing error."""
    selected_path = Path(selector).resolve()
    if selected_path.is_dir():
        return selected_path
    matches = [
        path
        for path in FIXTURES.iterdir()
        if path.name == selector or path.name.startswith(f"{selector}-")
    ]
    if len(matches) != 1:
        raise ValueError(f"fixture selector must match exactly one fixture: {selector}")
    return matches[0]


def load_config(fixture: Path) -> RunnerConfig:
    """Load fixture commands or return the built-in unittest convention."""
    config_path = fixture / "runner.toml"
    if not config_path.is_file():
        return RunnerConfig(
            visible=[sys.executable, "-m", "unittest", "discover", "-s", ".", "-v"],
            reference=[
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "oracle",
                "-v",
            ],
            visible_completion=UNITTEST_COMPLETION,
            reference_completion=UNITTEST_COMPLETION,
            visible_completion_stream="stderr",
            reference_completion_stream="stderr",
            manual_evidence_required=fixture.name.startswith("PG-E08-"),
            trusted_unittest=True,
        )

    with config_path.open("rb") as config_file:
        config = tomllib.load(config_file).get("runner", {})
    required = (
        "visible",
        "reference",
        "visible_completion",
        "reference_completion",
    )
    if any(name not in config for name in required):
        raise ValueError(f"runner.toml lacks required runner fields: {config_path}")
    for name in ("visible", "reference"):
        if not isinstance(config[name], list) or not config[name] or not all(
            isinstance(value, str) and value for value in config[name]
        ):
            raise ValueError(f"runner.{name} must be a non-empty string array")
    for name in ("visible_completion", "reference_completion"):
        if not isinstance(config[name], str) or not config[name]:
            raise ValueError(f"runner.{name} must be a non-empty regex string")
        try:
            expression = re.compile(config[name])
        except re.error as error:
            raise ValueError(f"runner.{name} is not a valid regex: {error}") from error
        if "evidence" not in expression.groupindex:
            raise ValueError(f"runner.{name} must define a named evidence group")
        if expression.search("") is not None:
            raise ValueError(f"runner.{name} must not match empty output")
    streams = {}
    for name in ("visible_completion_stream", "reference_completion_stream"):
        streams[name] = config.get(name, "combined")
        if streams[name] not in {"stdout", "stderr", "combined"}:
            raise ValueError(f"runner.{name} must be stdout, stderr, or combined")
    manual = config.get("manual_evidence_required", False)
    if not isinstance(manual, bool):
        raise ValueError("runner.manual_evidence_required must be true or false")
    return RunnerConfig(
        visible=config["visible"],
        reference=config["reference"],
        visible_completion=config["visible_completion"],
        reference_completion=config["reference_completion"],
        visible_completion_stream=streams["visible_completion_stream"],
        reference_completion_stream=streams["reference_completion_stream"],
        manual_evidence_required=manual,
    )


def resolve_command(command: list[str], cwd: Path) -> list[str]:
    """Resolve a fixture command without invoking a shell."""
    resolved = [sys.executable if value == "{python}" else value for value in command]
    requested = Path(resolved[0])
    executable = None
    if requested.is_absolute() and requested.is_file():
        executable = str(requested)
    elif "/" in resolved[0] or "\\" in resolved[0]:
        local_executable = (cwd / requested).resolve()
        if local_executable.is_file():
            executable = str(local_executable)
    else:
        executable = shutil.which(resolved[0])
    if executable is None:
        raise ValueError(f"gate executable is unavailable: {resolved[0]}")
    resolved[0] = str(Path(executable).resolve())
    return resolved


def prepare(args: Namespace) -> int:
    """Copy a fixture project into a fresh agent workspace."""
    fixture = resolve_fixture(args.fixture)
    workspace = Path(args.workspace).resolve()
    if workspace.is_relative_to(fixture):
        raise ValueError("workspace must be outside the selected fixture")
    shutil.copytree(
        fixture / "project",
        workspace,
        ignore=shutil.ignore_patterns("__pycache__", "*.py[cod]"),
    )
    print(f"workspace: {workspace}")
    print(f"task: {fixture / 'task.md'}")
    return 0


def workspace_inventory(workspace: Path) -> tuple[list[str], str]:
    """Return canonical per-file records and their aggregate SHA-256."""
    if not workspace.is_dir():
        raise ValueError(f"workspace is not a directory: {workspace}")
    records = []
    for path in workspace.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"workspace inventories do not follow symbolic links: {path}")
        if (
            not path.is_file()
            or path.suffix == ".pyc"
            or "__pycache__" in path.parts
        ):
            continue
        relative = path.relative_to(workspace).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest().upper()
        records.append(f"{relative} {digest}")
    records.sort()
    aggregate = hashlib.sha256("\n".join(records).encode()).hexdigest()
    return records, aggregate


def inventory(args: Namespace) -> int:
    """Print the canonical inventory of an existing workspace."""
    records, aggregate = workspace_inventory(Path(args.workspace).resolve())
    for record in records:
        print(record)
    print(f"inventory: {aggregate}")
    return 0


def changed_paths(baseline: Path, workspace: Path) -> list[str]:
    """Return byte-level additions, removals, and modifications."""

    def files(root: Path) -> set[Path]:
        return {
            path.relative_to(root)
            for path in root.rglob("*")
            if path.is_file() and path.suffix != ".pyc" and "__pycache__" not in path.parts
        }

    baseline_files = files(baseline)
    workspace_files = files(workspace)
    return sorted(
        path.as_posix()
        for path in baseline_files | workspace_files
        if not (baseline / path).is_file()
        or not (workspace / path).is_file()
        or (baseline / path).read_bytes() != (workspace / path).read_bytes()
    )


def run_gate(
    command: list[str], cwd: Path, environment: dict[str, str]
) -> subprocess.CompletedProcess[str]:
    """Execute one evaluator gate without interpreting or hiding its output."""
    return subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        capture_output=True,
        text=True,
        errors="replace",
        check=False,
        timeout=120,
    )


def gate_completed(
    result: subprocess.CompletedProcess[str], pattern: str, stream: str
) -> bool:
    """Return whether a gate emitted its evaluator-defined completion evidence."""
    output = {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "combined": f"{result.stdout}\n{result.stderr}",
    }[stream]
    match = re.search(pattern, output, re.DOTALL)
    return match is not None and bool(match.group("evidence"))


def write_unittest_wrapper(directory: Path, token: str) -> Path:
    """Create a trusted completion wrapper for the built-in unittest gates."""
    wrapper = directory / "unittest_gate.py"
    wrapper.write_text(
        "import sys\n"
        "import unittest\n"
        "program = unittest.main(module=None, argv=['unittest', *sys.argv[1:]], exit=False)\n"
        "result = program.result\n"
        "if result.testsRun > 0 and result.wasSuccessful():\n"
        f"    sys.__stderr__.write('PROOFGATE_UNITTEST_COMPLETE:{token}\\n')\n"
        "    raise SystemExit(0)\n"
        "raise SystemExit(1)\n",
        encoding="utf-8",
    )
    return wrapper


def gate_environment() -> dict[str, str]:
    """Return the minimum host environment needed by local Python gates."""
    allowed = (
        "COMSPEC",
        "HOME",
        "LANG",
        "LC_ALL",
        "PATH",
        "PATHEXT",
        "SYSTEMROOT",
        "TEMP",
        "TMP",
        "USERPROFILE",
        "WINDIR",
    )
    environment = {name: os.environ[name] for name in allowed if name in os.environ}
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONIOENCODING"] = "utf-8"
    return environment


def print_gate(
    name: str,
    command: list[str],
    cwd: Path,
    result: subprocess.CompletedProcess[str],
) -> None:
    """Print one gate's exact result and captured output."""
    print(f"{name} argv: {json.dumps(command)}")
    print(f"{name} cwd: {cwd}")
    print(f"{name}: exit {result.returncode}")
    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.stderr:
        print(result.stderr, end="" if result.stderr.endswith("\n") else "\n")


def evaluate(args: Namespace) -> int:
    """Run visible and public reference checks against a workspace."""
    fixture = resolve_fixture(args.fixture)
    config = load_config(fixture)
    workspace = Path(args.workspace).resolve()
    if not workspace.is_dir():
        raise ValueError(f"workspace is not a directory: {workspace}")

    _, aggregate = workspace_inventory(workspace)
    print(f"fixture: {fixture.name}")
    print(f"workspace: {workspace}")
    print(f"inventory: {aggregate}")
    changes = changed_paths(fixture / "project", workspace)
    print(f"changed: {', '.join(changes) if changes else 'none'}")

    environment = gate_environment()
    with tempfile.TemporaryDirectory() as directory:
        temporary = Path(directory)
        visible_workspace = temporary / "visible-workspace"
        reference_workspace = temporary / "reference-workspace"
        fixture_copy = temporary / "fixture"
        ignore = shutil.ignore_patterns("__pycache__", "*.py[cod]")
        shutil.copytree(workspace, visible_workspace, ignore=ignore)
        shutil.copytree(workspace, reference_workspace, ignore=ignore)
        shutil.copytree(fixture, fixture_copy, ignore=ignore)
        _, visible_before = workspace_inventory(visible_workspace)
        _, reference_before = workspace_inventory(reference_workspace)
        _, fixture_before = workspace_inventory(fixture_copy)

        visible_completion = config.visible_completion
        reference_completion = config.reference_completion
        if config.trusted_unittest:
            token = secrets.token_hex(32)
            wrapper = write_unittest_wrapper(temporary, token)
            command = [sys.executable, str(wrapper), *config.visible[3:]]
            reference_command = [sys.executable, str(wrapper), *config.reference[3:]]
            completion = rf"(?P<evidence>PROOFGATE_UNITTEST_COMPLETE:{token})"
            visible_completion = completion
            reference_completion = completion
        else:
            command = resolve_command(config.visible, visible_workspace)
            reference_command = resolve_command(config.reference, fixture_copy)

        visible = run_gate(command, visible_workspace, environment)
        print_gate("visible", command, visible_workspace, visible)

        reference_environment = environment.copy()
        reference_environment["PROOFGATE_FIXTURE_PROJECT"] = str(reference_workspace)
        reference = run_gate(reference_command, fixture_copy, reference_environment)
        print_gate("reference", reference_command, fixture_copy, reference)

        _, visible_after = workspace_inventory(visible_workspace)
        _, reference_after = workspace_inventory(reference_workspace)
        _, fixture_after = workspace_inventory(fixture_copy)
        mutated_gate = (
            visible_before != visible_after
            or reference_before != reference_after
            or fixture_before != fixture_after
        )

    if visible.returncode or reference.returncode:
        print("PROOFGATE: FAIL")
        return 1
    if not gate_completed(
        visible, visible_completion, config.visible_completion_stream
    ) or not gate_completed(
        reference,
        reference_completion,
        config.reference_completion_stream,
    ):
        print(
            "PROOFGATE: BLOCKED - a gate exited 0 but did not report a completed test run"
        )
        return 2
    if mutated_gate:
        print("PROOFGATE: BLOCKED - a gate modified its disposable workspace")
        return 2
    if config.manual_evidence_required:
        print(
            "PROOFGATE: BLOCKED - manual ask-before-edit checkpoint evidence is required"
        )
        return 2
    print("PROOFGATE: PASS")
    return 0


def build_parser() -> ArgumentParser:
    """Build the runner's public command-line parser."""
    parser = ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(required=True)
    prepare_parser = commands.add_parser(
        "prepare", help="create a fresh fixture workspace"
    )
    prepare_parser.add_argument("fixture")
    prepare_parser.add_argument("workspace")
    prepare_parser.set_defaults(handler=prepare)
    inventory_parser = commands.add_parser(
        "inventory", help="hash a completed workspace"
    )
    inventory_parser.add_argument("workspace")
    inventory_parser.set_defaults(handler=inventory)
    evaluate_parser = commands.add_parser(
        "evaluate", help="run visible and reference checks"
    )
    evaluate_parser.add_argument("fixture")
    evaluate_parser.add_argument("workspace")
    evaluate_parser.set_defaults(handler=evaluate)
    return parser


def main() -> int:
    """Execute the selected runner operation and return its process status."""
    args = build_parser().parse_args()
    try:
        return args.handler(args)
    except (OSError, subprocess.TimeoutExpired, ValueError) as error:
        print(f"BLOCKED: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
