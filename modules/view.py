from flask import render_template, request
from sqlalchemy import text

from modules import app
from modules.ctrla import DB, SongScraper
from modules.model import Album, Artist, Song

music_db = DB()
fresh = SongScraper().get_news()


@app.route("/")
def index():
    return render_template("index.html", fresh=fresh)


@app.route("/artists", methods=["GET", "POST"])
@app.route("/artists/<int:page>", methods=["GET"])
def artists_pg(page=1):
    if request.method == "POST":
        artist_name = request.form["artist_name"]
        music_db.insert_one(Artist(artist_name))

    _ = music_db.get_all(Artist).order_by(Artist.name).paginate(page=page, per_page=20)
    return render_template("artists.html", artists=_)


@app.route("/artist/<id_>", methods=["GET", "POST"])
def artists_profile_pg(id_: int):
    artist = music_db.find_by_id(Artist, id_)
    if request.method == "POST":
        _ = Album(request.form["album_title"], release_date=request.form["year"])
        artist.add_albums([_])

    return render_template("artist_profile.html", artist=artist)


@app.route("/albums", methods=["GET"])
@app.route("/albums/<int:page>", methods=["GET"])
def albums_pg(page=1):
    order_by = request.args.get("order_by")
    _ = music_db.get_all(Album, order_by=text(order_by)).join(Artist).paginate(page=page, per_page=20)
    return render_template("albums.html", albums=_, order_by=order_by)


@app.route("/album/<id_>", methods=["GET", "POST"])
def album_profile_pg(id_: int):
    if request.method == "GET":
        album = music_db.find_by_id(Album, id_)
        return render_template("album_profile.html", album=album, tracks=album.songs)
    else:
        song_name = request.form["song_name"]
        album = music_db.find_by_id(Album, id_)
        album.add_songs([Song(song_name)])
        return render_template("album_profile.html", album=album, tracks=album.songs)


@app.route("/songs")
def songs_pg():
    order_by = request.args.get("order_by")
    _ = music_db.get_all(Song, order_by=text(order_by)).join(Artist, Album)
    return render_template("songs.html", songs=_, order_by=order_by)


@app.route("/songs/<id_>", methods=["POST", "GET"])
def song_profile_pg(id_: int):
    song = music_db.find_by_id(Song, id_)
    if request.method == "POST":
        genius_url = request.form["genius_url"]
        song.add_lyrics(genius_url)

    return render_template("song_profile.html", song=song)


@app.route("/search", methods=["POST"])
def results_pg():
    if request.method == "POST":
        search_term = request.form["search_term"]
        results = {"artist_results": music_db.search(Artist.name, search_term),
                   "album_results": music_db.search(Album.title, search_term),
                   "song_results": music_db.search(Song.name, search_term)}
        return render_template("results.html", search_term=search_term, results=results)
