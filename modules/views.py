from datetime import datetime

from flask import render_template, request, url_for
from lyricsgenius import Genius
from sqlalchemy import text
from werkzeug.utils import redirect

from modules import app, db
from modules.ctrla import Ctrla
from modules.model import Album, Artist, Song

fresh = Ctrla().get_news()
genius = Genius()


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
                           artists=db.session.query(Artist).order_by(text(order_by)).paginate(page=page, per_page=20),
                           order_by=order_by)


@app.route("/artist")
def artist_():
    id_: int = request.args.get("id_")
    artist: Artist = db.session.query(Artist).get(id_)
    return render_template("artists/artist.html", artist=artist)


@app.route("/artist_create", methods=["POST"])
def artist_create():
    db.session.add(Artist(name=request.form["artist_name"],
                          profile_pic=request.form["profile_pic"],
                          genius_id=request.form["genius_id"]))
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
    album = db.session.query(Album).get(id_)
    return render_template("albums/album.html", album=album)


@app.route("/album_create", methods=["POST"])
def album_create():
    db.session.add(Album(title=request.form["album_name"],
                         cover_art=request.form["cover_art"],
                         genius_id=request.form["genius_id"],
                         artist=request.form["artist_id"],
                         release_date=datetime.strptime(request.form["release_date"],
                                                        "{'year': %Y, 'month': %m, 'day': %d}")))
    db.session.commit()

    return redirect(url_for("albums_"))


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
@app.route("/songs/<int:page>")
def songs_(page=1):
    order_by = request.args.get("order_by", default="songs_name")
    return render_template("songs/songs.html",
                           songs=db.session.query(Song).order_by(text(order_by)).join(Artist, Album).paginate(page=page,
                                                                                                              per_page=100),
                           order_by=order_by)


@app.route("/song")
def song_():
    id_: int = request.args.get("id_")
    song: Song = db.session.query(Song).get(id_)
    return render_template("songs/song.html", song=song)


@app.route("/top_100")
def top_100():
    return render_template("songs/top_100.html", top=top_100_)


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
        _ = genius.search_artists(search_term)["sections"][0]["hits"]

        return render_template("search.html",
                               search_term=search_term,
                               artist_results=_)


@app.route("/get_albums", methods=["POST", "GET"])
def get_albums():
    id_ = request.args.get("id_")
    _ = genius.artist_albums(id_)["albums"]
    return render_template("genius/get_albums.html", results=_)


@app.route("/get_songs")
def get_songs():
    id_ = request.args.get("id_")
    album: Album = db.session.query(Album).get(id_)

    for i in genius.album_tracks(album.genius_id)["tracks"]:
        db.session.add(Song(name=i["song"]["title"],
                            artist=album.artist,
                            album=album.id,
                            track_num=i["number"],
                            genius_id=i["song"]["id"]))

    db.session.commit()

    return redirect(url_for("album_", id_=id_))
