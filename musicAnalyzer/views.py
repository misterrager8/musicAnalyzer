from datetime import datetime

import praw
from flask import render_template, request, url_for, current_app
from lyricsgenius import Genius
from werkzeug.utils import redirect

from config import *
from musicAnalyzer import db
from musicAnalyzer.ctrla import Database
from musicAnalyzer.models import Artist, Album, Song

database = Database()
genius = Genius()

reddit = praw.Reddit(
    client_id=praw_client_id,
    client_secret=praw_client_secret,
    username=praw_username,
    password=praw_password,
    user_agent=praw_user_agent)


@current_app.template_filter()
def get_utc_time(time: float):
    return datetime.fromtimestamp(time).strftime("%m-%d-%y %I:%M %p")


@current_app.route("/")
def index():
    return render_template("index.html", posts=list(reddit.subreddit("HipHopHeads").hot(limit=25)))


@current_app.route("/artists", methods=["GET", "POST"])
def artists():
    if request.method == "GET":
        order_by = request.args.get("order_by", default="id desc")
        _ = database.search(Artist, order_by=order_by)
        return render_template("artists.html", artists=_, order_by=order_by)
    else:
        term = request.form["term"]
        return render_template("index.html", results=genius.search_artists(term)["sections"][0]["hits"])


@current_app.route("/artist")
def artist():
    _ = database.get(Artist, request.args.get("id_"))
    return render_template("artist.html", artist=_)


@current_app.route("/artist_search", methods=["POST"])
def artist_search():
    term = request.form["term"]
    return render_template("artist_search.html", results=genius.search_artists(term)["sections"][0]["hits"])


@current_app.route("/artist_create", methods=["POST"])
def artist_create():
    name = request.form["name"]
    genius_id = request.form["genius_id"] or None
    pic_url = request.form["pic_url"] or None
    database.add(Artist(name=name, genius_id=genius_id, pic_url=pic_url))

    return redirect(url_for("artists"))


@current_app.route("/artist_delete")
def artist_delete():
    _: Artist = database.get(Artist, request.args.get("id_"))
    database.delete(_)
    return redirect(request.referrer)


@current_app.route("/albums")
def albums():
    order_by = request.args.get("order_by", default="albums.title")
    _ = database.search(Album, order_by=order_by).join(Artist)
    return render_template("albums.html", albums=_, order_by=order_by)


@current_app.route("/album")
def album():
    _ = database.get(Album, request.args.get("id_"))
    return render_template("album.html", album=_)


@current_app.route("/album_create", methods=["POST", "GET"])
def album_create():
    if request.method == "POST":
        _: Artist = database.get(Artist, int(request.form["id_"]))

        title = request.form["title"]
        genius_id = request.form["genius_id"]
        cover_url = request.form["cover_url"]
        release_date = datetime.strptime(request.form["release_date"], "{'year': %Y, 'month': %m, 'day': %d}")

        album_ = Album(title=title, genius_id=genius_id, cover_url=cover_url, release_date=release_date, artist=_.id)
        database.add(album_)

        for idx, i in enumerate(album_.get_songs()):
            album_.songs.append(
                Song(title=i["song"]["title"], genius_url=i["song"]["id"], track_num=idx + 1, artist=_.id,
                     album=album_.id))

        db.session.commit()
        return redirect(request.referrer)
    else:
        _: Artist = database.get(Artist, int(request.args.get("id_")))
        return render_template("album_create.html", artist=_)


@current_app.route("/album_delete")
def album_delete():
    _: Album = database.get(Album, request.args.get("id_"))
    database.delete(_)
    return redirect(request.referrer)


@current_app.route("/songs")
def songs():
    order_by = request.args.get("order_by", default="songs.title")
    _ = database.search(Song, order_by=order_by).join(Artist, Album)
    return render_template("songs.html", songs=_, order_by=order_by)


@current_app.route("/song")
def song():
    _ = database.get(Song, request.args.get("id_"))
    return render_template("song.html", song=_)


@current_app.route("/song_create", methods=["POST"])
def song_create():
    _: Album = database.get(Album, int(request.form["id_"]))
    title = request.form["title"]

    database.add(Song(title=title, album=_.id, artist=_.artist))

    return redirect(request.referrer)


@current_app.route("/song_delete")
def song_delete():
    _: Song = database.get(Song, request.args.get("id_"))
    database.delete(_)
    return redirect(request.referrer)
