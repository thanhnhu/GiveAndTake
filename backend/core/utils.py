from datetime import datetime
from typing import Any


def to_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def to_int(value: str | None, default: int) -> int:
    try:
        return int(value) if value is not None else default
    except (TypeError, ValueError):
        return default


def dt(value: Any) -> str | None:
    """Convert a datetime (or None) to ISO-8601 string with Z suffix."""
    if isinstance(value, datetime):
        return value.isoformat().replace("+00:00", "Z")
    return str(value) if value is not None else None


def paginate(
    query: str,
    params: list[Any],
    page: int,
    page_size: int,
) -> tuple[str, list[Any]]:
    """Return (count_query, paged_params) for a paginated SELECT."""
    count_query = f"SELECT COUNT(*) FROM ({query}) _q"
    offset = (max(page, 1) - 1) * max(page_size, 1)
    return count_query, params + [max(page_size, 1), offset]
