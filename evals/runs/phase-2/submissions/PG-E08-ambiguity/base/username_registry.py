"""Profile heading used by the PG-E08 ambiguity fixture."""


def profile_header(user_id: int, name: str) -> str:
    """Return the user's display name followed by their hash-prefixed ID."""
    return f"{name} #{user_id}"
