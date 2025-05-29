#!/usr/bin/env python3
""" Basic Auth """
from api.v1.auth.auth import Auth
from models.user import User
from typing import Tuple, Optional
import base64
import binascii


class BasicAuth(Auth):
    """ Basic Authentication class """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Returns the Base64 part of the Authorization
        header for Basic Authentication
        """
        if authorization_header is None or not isinstance(
                    authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """
        Returns the decoded value of a Base64 string
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> Tuple[str, str]:
        """
        Returns the user email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None or not isinstance(
                                    decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on his email and password
        """
        if (not user_email or
                type(user_email) != str or
                not user_pwd or type(user_pwd) != str):
            return
        user = None
        try:
            user = User.search({"email": user_email})
        except Exception:
            return
        if not user:
            return
        for u in user:
            if u.is_valid_password(user_pwd):
                return u
     

    def current_user(self, request=None) -> Optional[User]:
        """
        Retrieves the User instance for a request using Basic Authentication
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        base64_part = self.extract_base64_authorization_header(auth_header)
        if base64_part is None:
            return None

        decoded = self.decode_base64_authorization_header(base64_part)
        if decoded is None:
            return None

        email, pwd = self.extract_user_credentials(decoded)
        if email is None or pwd is None:
            return None

        return self.user_object_from_credentials(email, pwd)
