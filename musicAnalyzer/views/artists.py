from flask import render_template, redirect, request, Blueprint
from musicAnalyzer import db
from lyricsgenius import Genius


artists = Blueprint("artists", __name__)

genius = Genius()


@artists.route("/artists", methods=["POST", "GET"])
def artists_():
    if request.method == "GET":
        return render_template("artists.html")
    else:
        term = request.form["name"]
        return render_template(
            "artists.html", results=genius.search_artists(term)["sections"][0]["hits"]
        )
