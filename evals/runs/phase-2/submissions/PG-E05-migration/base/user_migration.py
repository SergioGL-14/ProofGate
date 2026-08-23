"""In-memory user migration used by PG-E05."""

from collections.abc import Callable
from copy import deepcopy


Database = dict[str, object]


def migrate_users(database: Database, after_row: Callable[[int], None] | None = None) -> None:
    """Migrate version 1 user names to version 2, invoking after_row per row."""
    if database["schema_version"] != 1:
        raise ValueError("expected schema version 1")

    original = deepcopy(database)
    try:
        users = database["users"]
        for index, user in enumerate(users):
            user["display_name"] = user.pop("name")
            if after_row is not None:
                after_row(index)
        database["schema_version"] = 2
    except BaseException:
        database.clear()
        database.update(original)
        raise
