from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user
from musicAnalyzer.models import Blog
from musicAnalyzer import db
import datetime

blogs = Blueprint("blogs", __name__)


@blogs.route("/blogs")
def index():
    return render_template("blogs/blogs.html", blogs_=Blog.query.all())


@blogs.route("/blog")
def blog():
    blog_ = Blog.query.get(int(request.args.get("id_")))
    return render_template("blogs/blog.html", blog_=blog_)


@blogs.route("/create_blog", methods=["POST"])
def create_blog():
    blog_ = Blog(
        title=request.form["title"],
        date_published=datetime.datetime.now(),
        user_id=current_user.id,
    )
    db.session.add(blog_)
    db.session.commit()
    return redirect(url_for("blogs.editor", id_=blog_.id))


@blogs.route("/editor", methods=["GET", "POST"])
def editor():
    blog_ = Blog.query.get(int(request.args.get("id_")))
    if request.method == "POST":
        blog_.title = request.form["title"]
        blog_.content = request.form["content"]
        db.session.commit()
        return redirect(request.referrer)
    else:
        return render_template("blogs/editor.html", blog_=blog_)


@blogs.route("/delete_blog")
def delete_blog():
    blog_ = Blog.query.get(int(request.args.get("id_")))
    db.session.delete(blog_)
    db.session.commit()
    return redirect(request.referrer)
