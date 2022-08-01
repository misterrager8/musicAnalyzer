from flask import Blueprint, render_template, redirect, url_for, request
from musicAnalyzer.models import NewsItem
from musicAnalyzer import db
import datetime
from bs4 import BeautifulSoup
import requests

news = Blueprint("news", __name__)


@news.route("/news")
def index():
    return render_template(
        "news/news.html", news_=NewsItem.query.order_by(db.text("timestamp desc")).all()
    )


@news.route("/suggest_headline", methods=["POST"])
def suggest_headline():
    url = request.form["url"]
    title = BeautifulSoup(requests.get(url).text, "html.parser").find("title")

    return title.get_text()


@news.route("/post_news", methods=["POST"])
def post_news():
    newsitem_ = NewsItem(
        url=request.form["url"],
        headline=request.form["headline"],
        timestamp=datetime.datetime.now(),
    )

    db.session.add(newsitem_)
    db.session.commit()

    return redirect(request.referrer)


@news.route("/edit_news", methods=["POST"])
def edit_news():
    newsitem_ = NewsItem.query.get(int(request.args.get("id_")))
    newsitem_.url = request.form["url"]
    newsitem_.headline = request.form["headline"]
    newsitem_.timestamp = datetime.datetime.now()

    db.session.commit()

    return redirect(request.referrer)


@news.route("/delete_news")
def delete_news():
    newsitem_ = NewsItem.query.get(int(request.args.get("id_")))

    db.session.delete(newsitem_)
    db.session.commit()

    return redirect(request.referrer)
