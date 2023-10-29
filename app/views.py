from flask import Blueprint, render_template, request, url_for, redirect, session, flash, jsonify
from app.models import *
from functools import wraps

from db import db
from app import socketio

views = Blueprint('views', __name__, static_folder='static', template_folder='templates')

# NOTE, we create a new chat list for any newly registered user (the register route)


# Login decorator to ensure user is logged in before accessing certain routes
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("views.login"))
        return f(*args, **kwargs)

    return decorated


# Register a new user and hash password
@views.route("/register", methods=["GET", "POST"])
def register():
    """
    Handles user registration and password hashing.

    Returns:
        Response: Flask response object.
    """
    pass


@views.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles user login and session creation.

    Returns:
        Response: Flask response object.
    """
    pass
