# auth_log_decorator.py
"""
This script demonstrates the use of decorators for authentication and logging.
"""

import logging
import sqlite3
from functools import wraps
from pathlib import Path
from sqlite3 import Connection, Cursor
from typing import Any, Callable

# Create database file
db_file: Path = Path(__file__).parent / "users.db"
db_file.touch()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Database setup
def setup_database() -> None:
    conn: Connection = sqlite3.connect(database=db_file)
    cursor: Cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            authorized BOOLEAN NOT NULL
        )
    """
    )
    # Insert dummy data
    cursor.execute("INSERT OR REPLACE INTO users VALUES (101, 'Alice', 1)")
    cursor.execute("INSERT OR REPLACE INTO users VALUES (202, 'Bob', 0)")
    conn.commit()
    conn.close()


setup_database()


# Authentication Decorator
def authenticate(func) -> Callable[..., Any]:
    """Authenticates a user before accessing a function."""

    @wraps(wrapped=func)
    def wrapper(user_id, *args, **kwargs) -> Any:
        # Connect to database
        conn: Connection = sqlite3.connect(database=db_file)
        cursor: Cursor = conn.cursor()
        cursor.execute("SELECT authorized FROM users WHERE user_id = ?", (user_id,))
        user: Any = cursor.fetchone()
        conn.close()

        if not user:
            logging.warning(msg=f"User ID {user_id} does not exist.")
            return "User does not exist"
        if not user[0]:
            logging.warning(f"Unauthorized access attempt by user {user_id}")
            return "Access Denied"
        return func(user_id, *args, **kwargs)

    return wrapper


# Logging Decorator
def log_access(func) -> Callable[..., Any]:
    """Logs the access of a function."""

    @wraps(wrapped=func)
    def wrapper(*args, **kwargs) -> Any:
        logging.info(msg=f"Accessing: {func.__name__} with arguments: {args}, {kwargs}")
        return func(*args, **kwargs)

    return wrapper


# Multiple Decorators
@authenticate
@log_access
def view_profile(user_id) -> str:
    """Returns the profile of a given user."""

    # Connect to database
    conn: Connection = sqlite3.connect(database=db_file)
    cursor: Cursor = conn.cursor()
    cursor.execute("SELECT name FROM users WHERE user_id = ?", (user_id,))
    user: Any = cursor.fetchone()
    conn.close()
    return f"Profile of user {user_id}: {user[0]}"


# Usage
def main() -> None:
    print(view_profile(101))  # Authorized user
    print(view_profile(202))  # Unauthorized user
    print(view_profile(303))  # Non-existent user


if __name__ == "__main__":
    main()
