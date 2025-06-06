#!/usr/bin/env python3
"""
Defines a User model for SQLAlchemy representing the 'users' table.

This module is used to interact with the user records in the database.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    """
    SQLAlchemy User model representing the 'users' table.
    """
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(128), nullable=False)
    hashed_password: str = Column(String(128), nullable=False)
    session_id: str = Column(String(128), nullable=True)
    reset_token: str = Column(String(128), nullable=True)
