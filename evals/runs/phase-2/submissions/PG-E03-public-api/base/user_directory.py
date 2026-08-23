"""User lookup API and caller for the PG-E03 fixture."""


USERS = {1: "Ada", 2: "Grace"}


def _build_user_record(user_id: int, name: str) -> dict[str, object]:
    """Build the public record through the fixture's mutation seam."""
    return {"id": user_id, "name": name}


def get_user(user_id: int) -> dict[str, object]:
    """Return a new public user record for user_id, or raise KeyError."""
    return _build_user_record(user_id, USERS[user_id])


def profile_label(user_id: int) -> str:
    """Return the display label used by an existing profile caller."""
    user = get_user(user_id)
    return f"{user['name']} (#{user['id']})"
