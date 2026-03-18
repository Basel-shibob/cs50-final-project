from functools import wraps
from flask import render_template, session, redirect

def apology(message, code=400):
    return render_template("apology.html", message=message, code=code), code

def login_required(f):
    @wraps(f)
    def decorator_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorator_function