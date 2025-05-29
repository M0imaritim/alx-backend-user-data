#!/usr/bin/env python3
"""Session authentication with session stored in DB"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from models import storage


class SessionDBAuth(SessionExpAuth):
    """Session Authentication with persistent storage"""

    def create_session(self, user_id=None):
        """Create a session and store it in the database"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user ID using session ID from DB"""
        if session_id is None:
            return None

        from models.user_session import UserSession
        user_sessions = storage.search(UserSession)
        for session in user_sessions:
            if session.session_id == session_id:
                return session.user_id
        return None

    def destroy_session(self, request=None):
        """Destroy the UserSession in DB"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        from models.user_session import UserSession
        user_sessions = storage.search(UserSession)
        for session in user_sessions:
            if session.session_id == session_id:
                session.remove()
                return True
        return False
