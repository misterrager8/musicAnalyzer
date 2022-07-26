from flask import render_template, redirect, request, Blueprint
from musicAnalyzer.models import News
from musicAnalyzer import db
import datetime
import requests
from bs4 import BeautifulSoup


news = Blueprint("news", __name__)


@news.route("/news")
@news.route("/news/<int:page>")
def news_(page=1):
    return render_template(
        "news.html",
        news=News.query.order_by(db.text("timestamp desc")).paginate(
            page=page, per_page=15
        ),
    )


@news.route("/suggest_title", methods=["POST"])
def suggest_title():
    url = request.form["url"]
    title = (
        BeautifulSoup(requests.get(url).content, "html.parser").find("title").get_text()
    )

    return title


@news.route("/add_news", methods=["POST"])
def add_news():
    news_ = News(
        url=request.form["url"],
        headline=request.form["headline"],
        timestamp=datetime.datetime.now(),
    )

    db.session.add(news_)
    db.session.commit()

    return redirect(request.referrer)


@news.route("/edit_news", methods=["POST"])
def edit_news():
    news_ = News.query.get(int(request.form["id_"]))

    news_.url = request.form["url"]
    news_.headline = request.form["headline"]

    db.session.commit()

    return redirect(request.referrer)


@news.route("/delete_news")
def delete_news():
    news_ = News.query.get(int(request.args.get("id_")))

    db.session.delete(news_)
    db.session.commit()

    return redirect(request.referrer)
