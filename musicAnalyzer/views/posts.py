from flask import Blueprint, render_template, request
from flask_login import current_user
from werkzeug.utils import redirect
from bs4 import BeautifulSoup
import requests
from sqlalchemy import text

import datetime
from musicAnalyzer.ctrla import Database
from musicAnalyzer.models import Post

posts = Blueprint("posts", __name__)
database = Database()


@posts.route("/posts_/<int:page>")
@posts.route("/posts_")
def posts_(page=1):
    order_by = request.args.get("order_by", default="id desc")
    return render_template(
        "posts.html",
        order_by=order_by,
        all_posts=Post.query.order_by(text("date_posted desc")),
    )


@posts.route("/post_add", methods=["POST"])
def post_add():
    database.add(
        Post(
            title=request.form["title"],
            url=request.form["url"],
            date_posted=datetime.datetime.now(),
        )
    )
    return redirect(request.referrer)


@posts.route("/post_edit", methods=["POST"])
def post_edit():
    _: Post = database.get(Post, int(request.form["id_"]))
    _.url = request.form["url"]
    _.title = request.form["title"]

    database.update()
    return redirect(request.referrer)


@posts.route("/post_delete")
def post_delete():
    _: Post = database.get(Post, int(request.args.get("id_")))
    database.delete(_)

    return redirect(request.referrer)


@posts.route("/get_title", methods=["POST"])
def get_title():
    url = request.form["url"]
    title = BeautifulSoup(requests.get(url).text, "html.parser").find("title")

    return title.get_text()
