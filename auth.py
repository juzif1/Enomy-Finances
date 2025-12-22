
import hashlib
import os

from bottle import request

_sessions = {}

def hash_password(password: str) -> str:
    salt = "niemandx_salt"
    return hashlib.sha256((password + salt).encode()).hexdigest()

def login_user(user_id: int):
    session_id = hashlib.sha256(os.urandom(32)).hexdigest()
    _sessions[session_id] = user_id
    return session_id

def get_current_user():
    session_id = request.get_cookie("session_id")
    return _sessions.get(session_id)

def logout_user():
    session_id = request.get_cookie("session_id")
    _sessions.pop(session_id, None)
