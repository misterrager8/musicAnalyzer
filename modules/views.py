from datetime import datetime

import praw
import requests
from bs4 import BeautifulSoup
from flask import render_template, request, url_for
from sqlalchemy import text
from werkzeug.utils import redirect

from modules import app, db
from modules.model import Album, Artist, Song, Database

reddit = praw.Reddit("bot1")
database = Database()


def latest_news() -> list:
    return [i for i in reddit.subreddit("HipHopHeads").hot(limit=100) if not i.stickied]


def fresh_songs() -> list:
    return [i for i in reddit.subreddit("HipHopHeads").hot(limit=100) if "[FRESH" in i.title]


def get_top_100():
    _ = []
    soup = BeautifulSoup(requests.get("https://www.billboard.com/charts/hot-100").text, "html.parser")
    songs = soup.find_all("span", "chart-element__information__song")
    artists = soup.find_all("span", "chart-element__information__artist")

    for idx, i in enumerate(songs):
        _.append([songs[idx].get_text(), artists[idx].get_text()])

    return _


latest_news = latest_news()
fresh_songs = fresh_songs()
top_100_ = get_top_100()


@app.context_processor
def get_all():
    return dict(all_artists=db.session.query(Artist).all())


@app.route("/")
def index():
    return render_template("index.html",
                           latest_news=latest_news,
                           fresh_songs=fresh_songs)


@app.route("/artists")
@app.route("/artists/<int:page>")
def artists_(page=1):
    order_by = request.args.get("order_by", default="id desc")
    return render_template("artists/artists.html",
                           artists=database.search(Artist, order_by=order_by).paginate(page=page, per_page=20),
                           order_by=order_by)


@app.route("/artist")
def artist_():
    artist: Artist = database.get(Artist, request.args.get("id_"))
    return render_template("artists/artist.html", artist=artist)


@app.route("/artist_create", methods=["POST"])
def artist_create():
    database.create(Artist(name=request.form["artist_name"],
                           profile_pic=request.form["profile_pic"],
                           genius_id=request.form["genius_id"]))

    return redirect(request.referrer)


@app.route("/artist_update", methods=["POST"])
def artist_update():
    artist: Artist = database.get(Artist, request.args.get("id_"))

    artist.name = request.form["artist_name"]
    artist.profile_pic = request.form["profile_pic"]
    db.session.commit()

    return redirect(request.referrer)


@app.route("/artist_delete")
def artist_delete():
    artist: Artist = database.get(Artist, request.args.get("id_"))
    database.delete(artist)

    return redirect(url_for("artists_"))


@app.route("/albums")
@app.route("/albums/<int:page>")
def albums_(page=1):
    order_by = request.args.get("order_by", default="title")
    return render_template("albums/albums.html",
                           albums=database.search(Album, order_by=order_by).join(Artist).paginate(page=page,
                                                                                                  per_page=20),
                           order_by=order_by)


@app.route("/album")
def album_():
    album: Album = database.get(Album, request.args.get("id_"))
    return render_template("albums/album.html", album=album)


@app.route("/album_create", methods=["POST"])
def album_create():
    database.create(Album(title=request.form["album_name"],
                          cover_art=request.form["cover_art"],
                          genius_id=request.form["genius_id"],
                          artist=request.form["artist_id"],
                          release_date=datetime.strptime(request.form["release_date"],
                                                         "{'year': %Y, 'month': %m, 'day': %d}")))

    return redirect(request.referrer)


@app.route("/album_update", methods=["POST"])
def album_update():
    album: Album = database.get(Album, request.args.get("id_"))

    album.title = request.form["title"]
    album.release_date = request.form["release_date"]
    album.cover_art = request.form["cover_art"]
    db.session.commit()

    return redirect(request.referrer)


@app.route("/album_delete")
def album_delete():
    album: Album = database.get(Album, request.args.get("id_"))
    database.delete(album)

    return redirect(url_for("albums_"))


@app.route("/songs")
@app.route("/songs/<int:page>")
def songs_(page=1):
    order_by = request.args.get("order_by", default="songs_name")
    return render_template("songs/songs.html",
                           songs=db.session.query(Song).order_by(text(order_by)).join(Artist, Album).paginate(page=page,
                                                                                                              per_page=100),
                           order_by=order_by)


@app.route("/song")
def song_():
    song: Song = database.get(Song, request.args.get("id_"))
    return render_template("songs/song.html", song=song)


@app.route("/top_100")
def top_100():
    return render_template("songs/top_100.html", top=top_100_)


@app.route("/song_create", methods=["POST"])
def song_create():
    album: Album = database.get(Album, request.args.get("id_"))
    database.create(Song(name=request.form["song_name"],
                         track_num=int(request.form["track_num"]),
                         albums=album,
                         artists=album.artists))

    return redirect(url_for("album_", id_=album.id))


@app.route("/song_update", methods=["POST"])
def song_update():
    song: Song = database.get(Song, request.args.get("id_"))

    song.name = request.form["song_name"]
    song.track_num = int(request.form["track_num"])
    db.session.commit()

    return redirect(request.referrer)


@app.route("/song_delete")
def song_delete():
    song: Song = database.get(Song, request.args.get("id_"))
    database.delete(song)

    return redirect(url_for("songs_"))


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        search_term = request.form["search_term"]

        return render_template("search.html", search_term=search_term)
