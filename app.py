from curses import flash
import os
from cs50 import SQL
from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
import flask

# إعداد التطبيق
app = Flask(__name__)
app.config["SECRET_KEY"] = "any-long-random-string"  # ضيف السطر ده

# إعداد قاعدة البيانات
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    # الصفحة الرئيسية (هنعرض فيها الجدول لاحقاً)
    user_id = session["user_id"]

    user_data = db.execute("SELECT cash FROM users WHERE id = ?", user_id)

    if not user_data:
        session.clear()
        return redirect("/login")

    current_cash = user_data[0]["cash"]

    transactions = db.execute(
        "SELECT type, category, amount, description, date FROM transactions WHERE user_id = ? ORDER BY date DESC", user_id)
    return render_template("index.html", cash=current_cash, transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return apology("missing feilds")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]

        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    user_id = session["user_id"]
    if request.method == "POST":
        # جلب البيانات من الـ Form
        transaction_type = request.form.get("type")
        category = request.form.get("category")
        amount_raw = request.form.get("amount")
        description = request.form.get("description")

        if not transaction_type or not category or not amount_raw:
            return apology("Missing fields!")

        try:
            amount = float(amount_raw)
        except ValueError:
            return apology("Invalid amount")

        if amount <= 0:
            return apology("Amount must be positiv")

        # إضافة العملية لقاعدة البيانات (بافتراض user_id = 1 مؤقتاً لحد ما نعمل الـ login)

        cash_row = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = cash_row[0]["cash"]

        if transaction_type == "Expense":
            if amount > cash:
                return apology("Insufficient funds")
            cash -= amount
        elif transaction_type == "Income":
            cash += amount
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, user_id)
        db.execute("INSERT INTO transactions (user_id, type, category, amount, description) VALUES (?, ?, ?, ?, ?)",
                   user_id, transaction_type, category, amount, description)

        return redirect("/")
    else:
        return render_template("add.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username or not password or not confirmation:
            return apology("missing fields")
        if password != confirmation:
            return apology("passwords do not match")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) > 0:
            return apology("username unavailable")

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                   username, generate_password_hash(password))

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]

        flask.flash("Registered!")
        return redirect("/")
    else:
        return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
