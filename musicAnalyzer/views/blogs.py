from flask import render_template, redirect, request, Blueprint, url_for
from musicAnalyzer.models import Blog
from musicAnalyzer import db
import datetime
import requests
from bs4 import BeautifulSoup
from flask_login import current_user


blogs = Blueprint("blogs", __name__)


@blogs.route("/blogs")
def blogs_():
    return render_template(
        "blogs.html", blogs_=Blog.query.order_by(db.text("timestamp desc"))
    )


@blogs.route("/blog")
def blog():
    blog_ = Blog.query.get(int(request.args.get("id_")))
    return render_template("blog.html", blog_=blog_)


@blogs.route("/editor", methods=["POST", "GET"])
def editor():
    if request.method == "GET":
        return render_template(
            "editor.html", blog_=Blog.query.get(request.args.get("id_"))
        )
    else:
        blog_ = Blog.query.get(request.args.get("id_"))

        blog_.title = request.form["title"]
        blog_.content = request.form["content"]
        db.session.commit()

        return redirect(request.referrer)


@blogs.route("/add_blog", methods=["POST"])
def add_blog():
    blog_ = Blog(
        title=request.form["title"],
        timestamp=datetime.datetime.now(),
        user_id=current_user.id,
    )

    db.session.add(blog_)
    db.session.commit()

    return redirect(url_for("blogs.editor", id_=blog_.id))


@blogs.route("/delete_blog")
def delete_blog():
    blog_ = Blog.query.get(int(request.args.get("id_")))

    db.session.delete(blog_)
    db.session.commit()

    return redirect(request.referrer)
