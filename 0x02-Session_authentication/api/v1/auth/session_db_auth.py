#!/usr/bin/env python3
"""
SessionDBAuth module
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth handles session authentication with persistent DB storage.
    """

    def create_session(self, user_id=None):
        """
        Creates a session and stores it in the database.
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves a user ID based on a session ID from the database.
        """
        if session_id is None:
            return None
        try:
            sessions = UserSession.search({"session_id": session_id})
            for session in sessions:
                created_at = session.created_at
                if not created_at:
                    return None
                if self.session_duration <= 0:
                    return session.user_id
                if datetime.now() > created_at + timedelta(seconds=self.
                                                           session_duration):
                    return None
                return session.user_id
        except Exception:
            return None

    def destroy_session(self, request=None):
        """
        Deletes a user session from the database based on the request cookie.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        try:
            sessions = UserSession.search({"session_id": session_id})
            for session in sessions:
                session.remove()
            return True
        except Exception:
            return False
