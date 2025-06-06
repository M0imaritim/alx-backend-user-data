#!/usr/bin/env python3
"""DB module for managing the database connection and user operations."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User
from typing import Optional

VALID_FIELDS = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']


class DB:
    """
    DB class for handling database operations.

    Such as: adding, finding, and updating users.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance and create all tables."""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session: Optional[Session] = None

    @property
    def _session(self) -> Session:
        """Create and memoize a session object for interacting with the DB."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The user's email.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If email or hashed_password is not provided.
        """
        if not email or not hashed_password:
            raise ValueError("Email and hashed password must be provided.")
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by filtering with given keyword arguments.

        Returns:
            User: The matched User object.

        Raises:
            InvalidRequestError: If any keyword is not a valid User attribute.
            NoResultFound: If no matching user is found.
        """
        if not kwargs or any(key not in VALID_FIELDS for key in kwargs):
            raise InvalidRequestError("Invalid filter keys provided.")

        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise
        except Exception as e:
            raise InvalidRequestError(str(e))

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update attributes of a user with the given user_id.

        Args:
            user_id (int): ID of the user to update.
            kwargs: Attributes to update.

        Raises:
            ValueError: If any key in kwargs is not a valid User attribute.
        """
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if key not in VALID_FIELDS:
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)

        self._session.commit()
