"""Profile heading used by the PG-E08 ambiguity fixture."""


def profile_header(user_id: int, name: str) -> str:
    """Return the display name followed by the numeric ID as ``(#ID)``."""
    return f"{name} (#{user_id})"
