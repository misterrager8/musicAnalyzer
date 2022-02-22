from flask import Blueprint, render_template, request
from flask_login import current_user
from werkzeug.utils import redirect

from musicAnalyzer.ctrla import Database
from musicAnalyzer.models import Artist

artists = Blueprint("artists", __name__)
database = Database()


@artists.route("/artists_")
def artists_():
    order_by = request.args.get("order_by", default="id desc")
    return render_template("artists.html", order_by=order_by)


@artists.route("/artist_add", methods=["POST"])
def artist_add():
    database.add_multiple([Artist(name=i.title(),
                                  user_id=current_user.id) for i in request.form["name"].split(", ")])

    return redirect(request.referrer)


@artists.route("/artist")
def artist():
    _: Artist = database.get(Artist, request.args.get("id_"))
    return render_template("artist.html", artist=_)


@artists.route("/artist_edit", methods=["POST"])
def artist_edit():
    _: Artist = database.get(Artist, int(request.form["id_"]))
    _.name = request.form["name"]

    database.update()

    return redirect(request.referrer)


@artists.route("/artist_delete")
def artist_delete():
    _: Artist = database.get(Artist, request.args.get("id_"))

    database.delete_multiple([i for i in _.albums])
    database.delete_multiple([i for i in _.songs])
    database.delete(_)

    return redirect(request.referrer)
