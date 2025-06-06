#!/usr/bin/env python3
"""Auth module for handling user authentication."""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize the Auth instance with a database connection."""
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """
        Hash a password using bcrypt with automatic salting.

        Args:
            password (str): The plain-text password to hash.
        Returns:
            bytes: The salted hash of the password.
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

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
            hashed_pw = self._hash_password(password)
            return self._db.add_user(email, hashed_pw)
