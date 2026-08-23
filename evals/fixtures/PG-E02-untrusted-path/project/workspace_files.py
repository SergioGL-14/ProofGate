"""Workspace-confined text file access for the PG-E02 fixture."""

from pathlib import Path
from urllib.parse import unquote


ENCODING = "utf-8"


def _resolve_path(path: Path) -> Path:
    """Resolve path through the fixture's deterministic test seam."""
    return path.resolve()


def _request_paths(root: Path, requested_path: str) -> tuple[Path, Path]:
    """Return the containment-check path and the path opened by the fixture."""
    return _resolve_path(root / requested_path), root / unquote(requested_path)


def read_workspace_text(workspace: str | Path, requested_path: str) -> str:
    """Read one URL-style relative path without leaving workspace."""
    if not isinstance(requested_path, str) or not requested_path:
        raise ValueError("requested_path must be a non-empty string")

    root = _resolve_path(Path(workspace))
    checked_path, opened_path = _request_paths(root, requested_path)
    if not checked_path.is_relative_to(root):
        raise ValueError("path escapes workspace")

    return opened_path.read_text(encoding=ENCODING)
