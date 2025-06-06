#!/usr/bin/env python3
"""End-to-end integration test for user authentication service."""

import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Test user registration."""
    response = requests.post(f"{BASE_URL}/users", data={"email": email,
                                                        "password": password})
    assert response.status_code == 200 or response.status_code == 400
    if response.status_code == 200:
        assert response.json() == {"email": email, "message": "user created"}
    else:
        assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test login with incorrect password."""
    response = requests.post(f"{BASE_URL}/sessions",
                             data={"email": email, "password": password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test successful login. Returns session_id."""
    response = requests.post(f"{BASE_URL}/sessions",
                             data={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """Test accessing profile without being logged in."""
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test accessing profile with valid session."""
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """Test logout functionality."""
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies,
                               allow_redirects=False)
    assert response.status_code == 302  # redirect


def reset_password_token(email: str) -> str:
    """Test getting a reset password token."""
    response = requests.post(f"{BASE_URL}/reset_password",
                             data={"email": email})
    assert response.status_code == 200
    assert response.json().get("email") == email
    assert "reset_token" in response.json()
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test password update using reset token."""
    response = requests.put(f"{BASE_URL}/reset_password", data={
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    })
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


# Test data
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
