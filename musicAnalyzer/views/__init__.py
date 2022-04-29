from flask import current_app, render_template, url_for, request
from flask_login import logout_user, login_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from config import *
from musicAnalyzer import login_manager
from musicAnalyzer.ctrla import Database, GeniusWrapper, RedditWrapper
from musicAnalyzer.models import User

database = Database()
genius = GeniusWrapper()

reddit = RedditWrapper(
    client_id=praw_client_id,
    client_secret=praw_client_secret,
    username=praw_username,
    password=praw_password,
    user_agent=praw_user_agent)


@login_manager.user_loader
def load_user(id_: int):
    return User.query.get(id_)


@current_app.route("/")
def index():
    return render_template("index.html")


@current_app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user_: User = User.query.filter_by(username=username).first()

    if user_ and check_password_hash(user_.password, password):
        login_user(user_)
        return redirect(url_for("index"))
    else:
        return "Login failed."


@current_app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@current_app.route("/signup", methods=["POST"])
def signup():
    user_ = User(username=request.form["username"],
                 password=generate_password_hash(request.form["password"]))

    database.add(user_)
    login_user(user_)
    return redirect(url_for("index"))


@current_app.route("/profile")
def profile():
    return render_template("profile.html")


@current_app.route("/shuffle")
def shuffle():
    return render_template("shuffle.html")


@current_app.route("/user_edit", methods=["POST"])
def user_edit():
    current_user.username = request.form["username"]
    current_user.password = generate_password_hash(request.form["password"])
    database.update()

    return redirect(request.referrer)
