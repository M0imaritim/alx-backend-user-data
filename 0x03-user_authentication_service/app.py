#!/usr/bin/env python3
"""Basic Flask app."""
from flask import Flask, jsonify, request, abort, make_response
from auth import Auth

app = Flask(__name__)
auth = Auth()


@app.route("/", methods=["GET"])
def index():
    """
    GET '/'.

    Returns a welcome JSON message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """
    POST /users.

    Register a user with email and password from the form data.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        auth.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    POST /sessions.

    Creates a new session if login is valid.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if auth.valid_login(email, password):
        session_id = auth.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
