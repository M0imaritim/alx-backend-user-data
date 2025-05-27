#!/usr/bin/env python3
"""
Auth module for handling authentication
"""


from flask import request
from typing import List, TypeVar

User = TypeVar('User')


class Auth:
    """Auth class to manage API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if authentication is required for a given path
        """
        if path is None:
            return True

        if not excluded_paths or len(excluded_paths) == 0:
            return True

        path_with_slash = path if path.endswith('/') else path + '/'

        for excluded in excluded_paths:
            if excluded == path_with_slash:
                return False
            return True

    def authorization_header(self, request=None) -> str:
        """Returns the value of the authorization header from the request
        """
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None
        return auth_header

    def current_user(self, request=None) -> User:
        """Return the current user based on the request.
        """
        return None
