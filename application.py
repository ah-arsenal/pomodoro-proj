import os
import re
from flask_jsglue import JSGlue
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import time
import random
from helpers import *


# configure application
app = Flask(__name__)
JSGlue(app)



# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# config session
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///pomodoro.db")

@app.route("/")
@login_required
def index():
    # Return number of successful pomodoros at the bottom for that user on a given day so far.
    successful_pomodoros_day = (db.execute("SELECT COUNT(DISTINCT id) as cnt FROM history WHERE success = 'TRUE' AND user_id = :user_id AND ((DATETIME('now', '-1 day') <= DATETIME(created)));", user_id = session["user_id"])[0]['cnt'])
    successful_pomodoros_week = (db.execute("SELECT COUNT(DISTINCT id) as cnt FROM history WHERE success = 'TRUE' AND user_id = :user_id AND ((DATETIME('now', '-7 day') <= DATETIME(created)));", user_id = session["user_id"])[0]['cnt'])
    return render_template("index.html", successful_pomodoros_day = successful_pomodoros_day, successful_pomodoros_week = successful_pomodoros_week)

@app.route("/history")
@login_required
def history():
    # Return Pomodoro history (last 10) in descending order
    pomodoro_history = (db.execute("SELECT * FROM history WHERE user_id = :user_id ORDER BY created DESC LIMIT 10;", user_id = session["user_id"]))
    return render_template("history.html", pomodoro_history = pomodoro_history)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # ensure confirm password was submitted
        elif not request.form.get("confirm_password"):
            return apology("must provide password confirmation")

        # query database for username
        u_chk = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username not duplicate
        if len(u_chk) != 0:
            return apology("username already in use")

        # check passwords match
        if request.form.get("password") != request.form.get("confirm_password"):
            return apology("passwords must match")

        else:
        # insert user into database
            db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form["username"], hash=pwd_context.hash(request.form["password"]))

        # redirect user to home page
        return redirect(url_for("registered"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/registered", methods=["GET", "POST"])
def registered():
    return success()

@app.route("/startlog", methods=["GET"])
@login_required
def startlog():
    task_name = request.form["task_name"]
    console.log(task_name)
    db.execute("INSERT INTO history (user_id, task_name) VALUES (:user_id, :task_name);", user_id = session["user_id"], task_name = task_name)
    pass


@app.route("/successlog", methods=["GET"])
@login_required
def successlog():
    last_task_id = db.execute("SELECT id FROM history WHERE user_id = :user_id ORDER BY created DESC LIMIT 1;", user_id = session["user_id"])
    db.execute("UPDATE history SET success = TRUE WHERE id = :last_task_id;", last_task_id = last_task_id)
    pass

@app.route("/about")
def about():

    # redirect user to about page
    return render_template("about.html")