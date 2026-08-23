"""Authentication boundary for the PG-E06 fixture."""

import logging
from typing import Callable


AUTH_FAILURE_MESSAGE = "Authentication failed"


def _failure_log_event(username: str, password: str) -> tuple[str, tuple[object, ...]]:
    """Build the error log call through the fixture's mutation seam."""
    return "%s: username=%s password=%s", (AUTH_FAILURE_MESSAGE, username, password)


def authenticate(
    username: str,
    password: str,
    transport: Callable[[str, str], object],
    logger: logging.Logger,
) -> object:
    """Return the transport result, logging and re-raising transport errors."""
    try:
        return transport(username, password)
    except OSError:
        message, arguments = _failure_log_event(username, password)
        logger.error(message, *arguments)
        raise
