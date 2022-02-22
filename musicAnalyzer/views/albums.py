from flask import Blueprint, render_template, request
from flask_login import current_user
from werkzeug.utils import redirect

from musicAnalyzer.ctrla import Database
from musicAnalyzer.models import Album, Artist, Tag, AlbumTag

albums = Blueprint("albums", __name__)
database = Database()


@albums.route("/albums_")
def albums_():
    order_by = request.args.get("order_by", default="release_date desc")
    return render_template("albums.html", order_by=order_by)


@albums.route("/album_add", methods=["POST"])
def album_add():
    _: Artist = database.get(Artist, int(request.form["id_"]))
    database.add_multiple([Album(title=i.title(),
                                 artist_id=_.id,
                                 user_id=current_user.id) for i in request.form["title"].split(", ")])

    return redirect(request.referrer)


@albums.route("/album_edit", methods=["POST"])
def album_edit():
    _: Album = database.get(Album, int(request.form["id_"]))
    _.title = request.form["title"]
    _.release_date = request.form["release_date"]

    database.update()

    return redirect(request.referrer)


@albums.route("/album_tag")
def album_tag():
    album_: Album = database.get(Album, request.args.get("album_id"))
    tag_: Tag = database.get(Tag, request.args.get("tag_id"))

    database.add(AlbumTag(album_id=album_.id, tag_id=tag_.id))

    return redirect(request.referrer)


@albums.route("/album_untag")
def album_untag():
    _: AlbumTag = database.get(AlbumTag, request.args.get("id_"))

    database.delete(_)

    return redirect(request.referrer)


@albums.route("/album")
def album():
    _: Album = database.get(Album, request.args.get("id_"))
    return render_template("album.html", album=_)


@albums.route("/album_delete")
def album_delete():
    _: Album = database.get(Album, request.args.get("id_"))

    database.delete_multiple([i for i in _.songs])
    database.delete(_)

    return redirect(request.referrer)
