#!/usr/bin/env python3
"""
DB module for managing the database connection and user operations.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


VALID_FIELDS = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']


class DB:
    """
    DB class for handling database operations.
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance and create all tables.
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object for database access.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The user's email address.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The created user object.
        """
        if not email or not hashed_password:
            raise ValueError("Email and hashed_password are required.")

        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find the first user in the database that matches the provided criteria.

        Raises:
            InvalidRequestError: If any argument is not a valid field.
            NoResultFound: If no matching user is found.

        Returns:
            User: The matched user object.
        """
        if not kwargs:
            raise InvalidRequestError("No filter attributes provided.")

        for key in kwargs:
            if key not in VALID_FIELDS:
                raise InvalidRequestError(f"Invalid field: {key}")

        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise
        except InvalidRequestError:
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update attributes of a user with the given user_id.

        Args:
            user_id (int): The ID of the user to update.

        Raises:
            ValueError: If any provided attribute is invalid.
        """
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if key not in VALID_FIELDS:
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)

        self._session.commit()
