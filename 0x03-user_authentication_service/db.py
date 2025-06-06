#!/usr/bin/env python3
"""
DB module for managing the database connection and user operations.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


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
        """
        if not email or not hashed_password:
            return

        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find the first user in the database that matches the provided criteria.
        """
        if not kwargs:
            raise InvalidRequestError("No attributes provided to filter by.")

        try:
            user = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise
        except InvalidRequestError:
            raise

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update attributes of a user with the given user_id.
        """
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)

        self._session.commit()
