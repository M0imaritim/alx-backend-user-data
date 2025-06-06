#!/usr/bin/env python3
"""Auth module for handling user authentication."""

import bcrypt
import uuid 
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt with automatic salting.

    Args:
        password (str): The plain-text password to hash.
    Returns:
        bytes: The salted hash of the password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a new UUID."""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize the Auth instance with a database connection."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user if the email is not already in the database.

        Args:
            email (str): The user's email.
            password (str): The user's plain-text password.
        Returns:
            User: The newly created user object.
        Raises:
            ValueError: If a user already exists with the given email.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_pw = _hash_password(password)
            return self._db.add_user(email, hashed_pw)

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user credentials."""
        try:
            user = self._db.find_user_by(email=email)
            if user and bcrypt.checkpw(password.encode(),
                                       user.hashed_password):
                return True
        except Exception:
            pass
        return False

    def create_session(self, email: str) -> str:
        """Create a session ID for a user."""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return
