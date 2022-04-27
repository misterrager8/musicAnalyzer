from datetime import datetime

from flask import Blueprint, render_template, request
from flask_login import current_user
from lyricsgenius import Genius
from werkzeug.utils import redirect

from musicAnalyzer.ctrla import Database
from musicAnalyzer.models import Album, Artist, Tag, AlbumTag, Song

albums = Blueprint("albums", __name__)
database = Database()
genius = Genius()


@albums.route("/albums_/<int:page>")
@albums.route("/albums_")
def albums_(page=1):
    order_by = request.args.get("order_by", default="release_date desc")
    return render_template("albums.html",
                           order_by=order_by,
                           albums=current_user.get_albums(order_by=order_by).paginate(page=page, per_page=40))


@albums.route("/album_add", methods=["POST"])
def album_add():
    _: Artist = database.get(Artist, int(request.form["id_"]))

    title = request.form["title"]
    genius_id = request.form["genius_id"]
    release_date = datetime.strptime(request.form["release_date"], "{'year': %Y, 'month': %m, 'day': %d}")

    album_ = Album(title=title,
                   artist_id=_.id,
                   genius_id=genius_id,
                   release_date=release_date,
                   user_id=current_user.id)
    database.add(album_)

    for idx, i in enumerate(genius.album_tracks(album_.genius_id)["tracks"]):
        album_.songs.append(
            Song(name=i["song"]["title"],
                 genius_id=i["song"]["id"],
                 track_num=idx + 1,
                 artist_id=_.id,
                 album_id=album_.id,
                 user_id=current_user.id))

    database.update()
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
    album_: Album = database.get(Album, int(request.args.get("album_id")))
    tag_: Tag = database.get(Tag, int(request.args.get("tag_id")))

    database.add(AlbumTag(album_id=album_.id, tag_id=tag_.id))

    return redirect(request.referrer)


@albums.route("/album_untag")
def album_untag():
    _: AlbumTag = database.get(AlbumTag, int(request.args.get("id_")))

    database.delete(_)

    return redirect(request.referrer)


@albums.route("/album")
def album():
    _: Album = database.get(Album, int(request.args.get("id_")))
    return render_template("album.html", album=_)


@albums.route("/album_delete")
def album_delete():
    _: Album = database.get(Album, int(request.args.get("id_")))

    database.delete_multiple([i for i in _.songs])
    database.delete_multiple([i for i in _.get_tags()])
    database.delete(_)

    return redirect(request.referrer)
