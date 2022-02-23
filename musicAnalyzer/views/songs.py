from flask import Blueprint, render_template, request
from flask_login import current_user
from werkzeug.utils import redirect

from musicAnalyzer.ctrla import Database
from musicAnalyzer.models import Song, Album

songs = Blueprint("songs", __name__)
database = Database()


@songs.route("/songs_/<int:page>")
@songs.route("/songs_")
def songs_(page=1):
    order_by = request.args.get("order_by", default="id desc")
    return render_template("songs.html",
                           order_by=order_by,
                           songs=current_user.get_songs(order_by=order_by).paginate(page=page, per_page=50))


@songs.route("/song_add", methods=["POST"])
def song_add():
    _: Album = database.get(Album, int(request.form["id_"]))
    database.add_multiple([Song(name=i.title(),
                                album_id=_.id,
                                artist_id=_.artist_id,
                                user_id=current_user.id) for i in request.form["name"].split(", ")])

    return redirect(request.referrer)


@songs.route("/song")
def song():
    _: Song = database.get(Song, int(request.args.get("id_")))
    return render_template("song.html", song=_)


@songs.route("/song_rate")
def song_rate():
    _: Song = database.get(Song, int(request.args.get("id_")))

    _.rating = request.args.get("rating")
    database.update()
    return redirect(request.referrer)


@songs.route("/song_delete")
def song_delete():
    _: Song = database.get(Song, int(request.args.get("id_")))
    database.delete(_)

    return redirect(request.referrer)
