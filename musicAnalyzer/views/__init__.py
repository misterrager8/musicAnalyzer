from flask import render_template, current_app, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from musicAnalyzer.models import News, User
from musicAnalyzer import db, login_manager
from musicAnalyzer import scraper
from musicAnalyzer.scraper import Link
import datetime
from praw import Reddit
import billboard
from lyricsgenius import Genius
from werkzeug.security import check_password_hash, generate_password_hash

genius = Genius()

reddit_ = Reddit(
    client_id=current_app.config["PRAW_CLIENT_ID"],
    client_secret=current_app.config["PRAW_CLIENT_SECRET"],
    username=current_app.config["PRAW_USERNAME"],
    password=current_app.config["PRAW_PASSWORD"],
    user_agent=current_app.config["PRAW_USER_AGENT"],
)


@login_manager.user_loader
def load_user(id_: int):
    return User.query.get(id_)


@current_app.route("/")
def index():
    return render_template(
        "index.html",
        news=News.query.order_by(db.text("timestamp desc")).all(),
        chart=billboard.ChartData("rap-songs")[:10],
        fresh=[
            i
            for i in reddit_.subreddit("HipHopHeads").hot(limit=50)
            if "FRESH" in i.title
        ],
    )


@current_app.route("/admin")
def admin():
    return render_template(
        "admin.html",
        links_=scraper.get_links()
        + [
            Link(i.url, "HipHopHeads", i.title)
            for i in reddit_.subreddit("HipHopHeads").hot(limit=50)
            if not i.is_self
        ],
    )


@current_app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    user_ = User.query.filter(User.email == email).first()

    if user_ and check_password_hash(user_.password, password):
        login_user(user_)
        return redirect(url_for("index"))
    else:
        return "Login failed"


@current_app.route("/signup", methods=["POST"])
def signup():
    user_ = User(
        email=request.form["email"],
        password=generate_password_hash(request.form["password"]),
        date_created=datetime.datetime.now(),
    )
    db.session.add(user_)
    db.session.commit()
    login_user(user_)

    return redirect(url_for("index"))


@current_app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
