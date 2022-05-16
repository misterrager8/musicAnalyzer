from flask import Blueprint, render_template, request
from flask_login import current_user
from werkzeug.utils import redirect

import datetime
from musicAnalyzer.ctrla import Database
from musicAnalyzer.models import Post

posts = Blueprint("posts", __name__)
database = Database()


@posts.route("/posts_/<int:page>")
@posts.route("/posts_")
def posts_(page=1):
    order_by = request.args.get("order_by", default="id desc")
    return render_template("posts.html", order_by=order_by, all_posts=Post.query)


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
    return redirect(request.referrer)


@posts.route("/post_delete")
def post_delete():
    _: Post = database.get(Post, int(request.args.get("id_")))
    database.delete(_)

    return redirect(request.referrer)
