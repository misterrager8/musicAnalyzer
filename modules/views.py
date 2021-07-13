from flask import render_template, request, url_for
from lyricsgenius import Genius
from sqlalchemy import text
from werkzeug.utils import redirect

from modules import app, db
from modules.ctrla import RedditWrapper
from modules.model import Album, Artist, Song

fresh = RedditWrapper().get_news()
x = Genius()


@app.route("/")
def index():
    return render_template("index.html", fresh=fresh)


@app.route("/artists")
@app.route("/artists/<int:page>")
def artists_(page=1):
    return render_template("artists/artists.html",
                           artists=db.session.query(Artist).order_by(Artist.name).paginate(page=page, per_page=20))


@app.route("/artist")
def artist_():
    id_: int = request.args.get("id_")
    artist = x.search_artist(None, artist_id=id_, max_songs=0)
    artist_albums = x.artist_albums(artist.id)
    return render_template("artists/artist.html", artist=artist, artist_albums=artist_albums)


@app.route("/artist_create", methods=["POST"])
def artist_create():
    db.session.add(Artist(name=request.form["artist_name"]))
    db.session.commit()

    return redirect(url_for("artists_"))


@app.route("/artist_update", methods=["POST"])
def artist_update():
    id_: int = request.args.get("id_")
    artist: Artist = db.session.query(Artist).get(id_)

    artist.name = request.form["artist_name"]
    artist.profile_pic = request.form["profile_pic"]
    db.session.commit()

    return redirect(url_for("artist_", id_=id_))


@app.route("/artist_delete")
def artist_delete():
    id_: int = request.args.get("id_")
    artist: Artist = db.session.query(Artist).get(id_)

    db.session.delete(artist)
    db.session.commit()

    return redirect(url_for("artists_"))


@app.route("/albums")
@app.route("/albums/<int:page>")
def albums_(page=1):
    order_by = request.args.get("order_by", default="title")
    return render_template("albums/albums.html",
                           albums=db.session.query(Album).order_by(text(order_by)).join(Artist).paginate(page=page,
                                                                                                         per_page=20),
                           order_by=order_by)


@app.route("/album")
def album_():
    id_: int = request.args.get("id_")
    album = x.search_album(None, album_id=id_, get_full_info=False)
    return render_template("albums/album.html", album=album)


@app.route("/album_create", methods=["POST"])
def album_create():
    id_: int = request.args.get("id_")
    artist: Artist = db.session.query(Artist).get(id_)

    db.session.add(Album(title=request.form["title"],
                         release_date=request.form["release_date"],
                         artists=artist))
    db.session.commit()

    return redirect(url_for("artist_", id_=artist.id))


@app.route("/album_update", methods=["POST"])
def album_update():
    id_: int = request.args.get("id_")
    album: Album = db.session.query(Album).get(id_)

    album.title = request.form["title"]
    album.release_date = request.form["release_date"]
    album.cover_art = request.form["cover_art"]
    db.session.commit()

    return redirect(url_for("album_", id_=id_))


@app.route("/album_delete")
def album_delete():
    id_: int = request.args.get("id_")
    album: Album = db.session.query(Album).get(id_)

    db.session.delete(album)
    db.session.commit()

    return redirect(url_for("albums_"))


@app.route("/songs")
def songs_():
    order_by = request.args.get("order_by", default="songs_name")
    return render_template("songs/songs.html",
                           songs=db.session.query(Song).order_by(text(order_by)).join(Artist, Album),
                           order_by=order_by)


@app.route("/song")
def song_():
    id_: int = request.args.get("id_")
    song: Song = db.session.query(Song).get(id_)
    return render_template("songs/song.html", song=song)


@app.route("/song_create", methods=["POST"])
def song_create():
    id_: int = request.args.get("id_")
    album: Album = db.session.query(Album).get(id_)

    db.session.add(Song(name=request.form["song_name"],
                        track_num=int(request.form["track_num"]),
                        albums=album,
                        artists=album.artists))
    db.session.commit()

    return redirect(url_for("album_", id_=album.id))


@app.route("/song_update", methods=["POST"])
def song_update():
    id_: int = request.args.get("id_")
    song: Song = db.session.query(Song).get(id_)

    song.name = request.form["song_name"]
    song.track_num = int(request.form["track_num"])
    db.session.commit()

    return redirect(url_for("song_", id_=id_))


@app.route("/song_delete")
def song_delete():
    id_: int = request.args.get("id_")
    song: Song = db.session.query(Song).get(id_)

    db.session.delete(song)
    db.session.commit()

    return redirect(url_for("songs_"))


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        search_term = request.form["search_term"]

        return render_template("search.html", search_term=search_term,
                               result=x.search_artist(search_term, max_songs=0, allow_name_change=False))
