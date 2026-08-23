"""Text report export used by the PG-E09 real-boundary fixture."""

from collections.abc import Callable, Iterable
from pathlib import Path
from typing import TextIO


def render_report(rows: Iterable[str]) -> str:
    """Render one report row per line with a final newline."""
    return "".join(f"{row}\n" for row in rows)


def export_report(
    path: str | Path,
    rows: Iterable[str],
    *,
    opener: Callable[..., TextIO] = open,
) -> None:
    """Write rows as UTF-8 text to path using an injectable text opener."""
    with opener(path, "w", encoding="utf-8") as stream:
        stream.write(render_report(rows))
