from datetime import datetime

from flask import render_template, request, url_for
from lyricsgenius import Genius
from werkzeug.utils import redirect

from musicAnalyzer import app, db
from musicAnalyzer.ctrla import Database
from musicAnalyzer.models import Artist, Album, Song

database = Database()
genius = Genius()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/artists", methods=["GET", "POST"])
def artists():
    if request.method == "GET":
        order_by = request.args.get("order_by", default="id desc")
        _ = database.search(Artist, order_by=order_by)
        return render_template("artists.html", artists=_, order_by=order_by)
    else:
        term = request.form["term"]
        return render_template("index.html", results=genius.search_artists(term)["sections"][0]["hits"])


@app.route("/artist")
def artist():
    _ = database.get(Artist, request.args.get("id_"))
    return render_template("artist.html", artist=_)


@app.route("/artist_create", methods=["POST"])
def artist_create():
    name = request.form["name"]
    genius_id = request.form["genius_id"] or None
    pic_url = request.form["pic_url"] or None
    database.add(Artist(name=name, genius_id=genius_id, pic_url=pic_url))

    return redirect(url_for("artists"))


@app.route("/artist_update", methods=["POST"])
def artist_update():
    _: Artist = database.get(Artist, int(request.form["id_"]))

    _.name = request.form["name"]
    _.genius_id = request.form["genius_id"] or None
    db.session.commit()

    return redirect(request.referrer)


@app.route("/artist_delete")
def artist_delete():
    _: Artist = database.get(Artist, request.args.get("id_"))
    database.delete(_)
    return redirect(request.referrer)


@app.route("/albums")
def albums():
    order_by = request.args.get("order_by", default="albums.title")
    _ = database.search(Album, order_by=order_by).join(Artist)
    return render_template("albums.html", albums=_, order_by=order_by)


@app.route("/album")
def album():
    _ = database.get(Album, request.args.get("id_"))
    return render_template("album.html", album=_)


@app.route("/album_create", methods=["POST", "GET"])
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


@app.route("/album_update", methods=["POST"])
def album_update():
    _: Album = database.get(Album, int(request.form["id_"]))

    _.title = request.form["title"]
    _.release_date = request.form["release_date"] or None
    _.release_type = request.form["release_type"]
    db.session.commit()

    return redirect(request.referrer)


@app.route("/album_delete")
def album_delete():
    _: Album = database.get(Album, request.args.get("id_"))
    database.delete(_)
    return redirect(request.referrer)


@app.route("/songs")
def songs():
    order_by = request.args.get("order_by", default="songs.title")
    _ = database.search(Song, order_by=order_by).join(Artist, Album)
    return render_template("songs.html", songs=_, order_by=order_by)


@app.route("/song")
def song():
    _ = database.get(Song, request.args.get("id_"))
    return render_template("song.html", song=_)


@app.route("/song_create", methods=["POST"])
def song_create():
    _: Album = database.get(Album, int(request.form["id_"]))
    title = request.form["title"]

    database.add(Song(title=title, album=_.id, artist=_.artist))

    return redirect(request.referrer)


@app.route("/song_update", methods=["POST"])
def song_update():
    _: Song = database.get(Song, int(request.form["id_"]))

    _.title = request.form["title"]
    _.rating = int(request.form["rating"])
    _.track_num = int(request.form["track_num"] or 0)
    db.session.commit()

    return redirect(request.referrer)


@app.route("/song_delete")
def song_delete():
    _: Song = database.get(Song, request.args.get("id_"))
    database.delete(_)
    return redirect(request.referrer)
