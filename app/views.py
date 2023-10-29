from flask import Blueprint, render_template, request, url_for, redirect, session, flash, jsonify
from app.models import *
from functools import wraps

from db import db
from app import socketio

views = Blueprint('views', __name__, static_folder='static', template_folder='templates')