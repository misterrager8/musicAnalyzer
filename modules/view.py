from flask import render_template, request
from sqlalchemy import text

from modules import app, db
from modules.ctrla import DB, SongScraper
from modules.model import Album, Artist, Song

music_db = DB()
y = SongScraper()

songs = music_db.get_all(Song)

news = y.get_news()


def refresh(item_type):
    for i in music_db.get_all(item_type): db.session.refresh(i)


@app.route("/")
def index():
    return render_template("index.html", fresh=news)


@app.route("/artists", methods=["GET"])
@app.route("/artists/<int:page>", methods=["GET"])
def artists_pg(page=1):
    _ = music_db.get_all(Artist).order_by(Artist.name).paginate(page=page, per_page=20)
    return render_template("artists.html", artists=_)


@app.route("/artist/<id_>")
def artists_profile_pg(id_: int):
    artist = music_db.find_by_id(Artist, id_)
    return render_template("artist_profile.html", artist=artist)


@app.route("/albums", methods=["GET"])
@app.route("/albums/<int:page>", methods=["GET"])
def albums_pg(page=1):
    order_by = request.args.get("order_by")
    _ = music_db.get_all(Album, order_by=text(order_by)).join(Artist).paginate(page=page, per_page=20)
    return render_template("albums.html", albums=_, order_by=order_by)


@app.route("/album/<id_>")
def album_profile_pg(id_: int):
    album = music_db.find_by_id(Album, id_)
    _ = album.songs
    return render_template("album_profile.html", album=album, tracks=_)


@app.route("/songs")
def songs_pg():
    return render_template("songs.html", songs=songs)


@app.route("/songs/<id_>")
def song_profile_pg(id_: int):
    song = music_db.find_by_id(Song, id_)
    return render_template("song_profile.html", song=song)


@app.route("/search", methods=["POST"])
def results_pg():
    if request.method == "POST":
        search_term = request.form["search_term"]
        results = {"artist_results": music_db.search(Artist.name, search_term),
                   "album_results": music_db.search(Album.title, search_term),
                   "song_results": music_db.search(Song.name, search_term)}
        return render_template("results.html", search_term=search_term, results=results)


@app.route("/edit<id_>", methods=["POST"])
def edit(id_: int):
    if request.method == "POST":
        artist = music_db.find_by_id(Artist, id_)
        _ = Album(request.form["album_title"], release_date=request.form["year"])
        artist.add_albums([_])
        refresh(Artist)
        return render_template("artist_profile.html", artist=artist)
