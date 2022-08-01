from flask import render_template, current_app, redirect, request, url_for
from musicAnalyzer import db, login_manager, scraper
from musicAnalyzer.models import User, NewsItem
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import billboard
from datetime import datetime
from praw import Reddit

reddit_ = Reddit(
    client_id=current_app.config["CLIENT_ID"],
    client_secret=current_app.config["CLIENT_SECRET"],
    username=current_app.config["USERNAME"],
    password_=current_app.config["PASSWORD_"],
    user_agent=current_app.config["USER_AGENT"],
)


@current_app.context_processor
def convert_utc():
    def utc_to_time(utc):
        return datetime.utcfromtimestamp(utc)

    return dict(utc_to_time=utc_to_time)


@login_manager.user_loader
def load_user(id_: int):
    return User.query.get(id_)


@current_app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user_ = User.query.filter(User.username == username).first()
    if user_ and check_password_hash(user_.password, password):
        login_user(user_)
        return redirect(url_for("index"))
    else:
        return "Login failed."


@current_app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]

    user_ = User(username=username, password=generate_password_hash(password))
    db.session.add(user_)
    db.session.commit()
    login_user(user_)

    return redirect(url_for("index"))


@current_app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@current_app.route("/")
def index():
    return render_template(
        "index.html",
        news_=NewsItem.query.order_by(db.text("timestamp desc")).all(),
        charts=billboard.ChartData("rap-songs"),
        hot=[
            i
            for i in reddit_.subreddit("HipHopHeads").hot(limit=50)
            if "FRESH" in i.title
        ],
    )


@current_app.route("/admin")
def admin():
    return render_template("admin.html", links_=scraper.get_links())
