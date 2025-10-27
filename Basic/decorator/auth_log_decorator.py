# auth_log_decorator.py
"""
This script demonstrates the use of decorators for authentication and logging.
"""

import logging
import sqlite3
from functools import wraps
from pathlib import Path
from sqlite3 import Cursor
from typing import Any, Callable

# Create database file
db_file: Path = Path(__file__).parent / "users.db"
db_file.touch()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def setup_database() -> None:
    """Setup database."""
    try:
        with sqlite3.connect(database=db_file) as conn:
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
            records: list[tuple[int, str, int]] = [
                (101, "Alice", 1),
                (202, "Bob", 0),
            ]
            cursor.executemany("INSERT OR REPLACE INTO users VALUES (?, ?, ?)", records)
            conn.commit()
            cursor.close()
            logging.info("Database setup complete.")
    except sqlite3.Error as e:
        logging.error(f"Error creating database: {e}")


# Setup database
setup_database()


# Authentication Decorator
def authenticate(func) -> Callable[..., Any]:
    """Authenticates a user before accessing a function."""

    @wraps(wrapped=func)
    def wrapper(user_id, *args, **kwargs) -> Any:
        try:
            # Connect to database
            with sqlite3.connect(database=db_file) as conn:
                cursor: Cursor = conn.cursor()
                cursor.execute(
                    "SELECT authorized FROM users WHERE user_id = ?", (user_id,)
                )
                user: Any = cursor.fetchone()
                cursor.close()

                if not user:
                    logging.warning(msg=f"User ID {user_id} does not exist.")
                    return "User does not exist"
                if not user[0]:
                    logging.warning(f"Unauthorized access attempt by user {user_id}")
                    return "Access Denied"
                return func(user_id, *args, **kwargs)
        except sqlite3.Error as e:
            logging.error(f"Error accessing database: {e}")
            return "Error accessing database"

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
    try:
        # Connect to database
        with sqlite3.connect(database=db_file) as conn:
            cursor: Cursor = conn.cursor()
            cursor.execute("SELECT name FROM users WHERE user_id = ?", (user_id,))
            user: Any = cursor.fetchone()
            cursor.close()
        return f"Profile of user {user_id}: {user[0]}"
    except Exception as e:
        logging.error(f"Error accessing profile: {e}")
        return "Error accessing profile"


# Usage
def main() -> None:
    print(view_profile(101))  # Authorized user
    print(view_profile(202))  # Unauthorized user
    print(view_profile(303))  # Non-existent user


if __name__ == "__main__":
    main()
