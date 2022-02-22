from flask import Blueprint, render_template, request
from flask_login import current_user
from lyricsgenius import Genius
from werkzeug.utils import redirect

from musicAnalyzer.ctrla import Database
from musicAnalyzer.models import Artist

artists = Blueprint("artists", __name__)
database = Database()
genius = Genius()


@artists.route("/artists_", methods=["POST", "GET"])
def artists_():
    if request.method == "GET":
        order_by = request.args.get("order_by", default="id desc")
        return render_template("artists.html", order_by=order_by)
    else:
        term = request.form["name"]
        return render_template("artists.html", results=genius.search_artists(term)["sections"][0]["hits"])


@artists.route("/artist_add", methods=["POST"])
def artist_add():
    _ = Artist(name=request.form["name"],
               genius_id=request.form["genius_id"],
               user_id=current_user.id)
    database.add(_)

    return render_template("artist.html", artist=_, get=True)


@artists.route("/artist", methods=["GET", "POST"])
def artist():
    if request.method == "GET":
        _: Artist = database.get(Artist, int(request.args.get("id_")))
        return render_template("artist.html", artist=_, get=True)
    else:
        _: Artist = database.get(Artist, int(request.form["id_"]))
        return render_template("artist.html", artist=_, results=genius.artist_albums(_.genius_id)["albums"])


@artists.route("/artist_edit", methods=["POST"])
def artist_edit():
    _: Artist = database.get(Artist, int(request.form["id_"]))
    _.name = request.form["name"]

    database.update()

    return redirect(request.referrer)


@artists.route("/artist_delete")
def artist_delete():
    _: Artist = database.get(Artist, int(request.args.get("id_")))

    database.delete_multiple([i for i in _.albums])
    database.delete_multiple([i for i in _.songs])
    database.delete(_)

    return redirect(request.referrer)
