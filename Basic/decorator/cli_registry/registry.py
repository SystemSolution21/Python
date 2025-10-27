from functools import wraps
from typing import Any, Callable

_registry: list[tuple[str, str, Callable[..., Any]]] = []


def register_command(group: str, name: str) -> Callable[..., Any]:
    """Register a command."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(wrapped=func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        _registry.append((group, name, wrapper))
        return wrapper

    return decorator


def get_registry() -> list[tuple[str, str, Callable[..., Any]]]:
    """Get the registry."""
    return _registry.copy()
