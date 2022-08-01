from flask import Blueprint, render_template, request
from lyricsgenius import Genius
from musicAnalyzer.models import Artist

artists = Blueprint("artists", __name__)
genius = Genius()


@artists.route("/artists", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("artists/artists.html")
    else:
        term = request.form["artist"]
        return render_template(
            "artists/artists.html",
            results=genius.search_artists(term)["sections"][0]["hits"],
        )


@artists.route("/artist")
def artist():
    _ = genius.artist(int(request.args.get("genius_id")))
    artist_ = Artist(
        int(_["artist"]["id"]),
        _["artist"]["name"],
        genius.artist_albums(int(_["artist"]["id"])),
    )
    return render_template("artists/artist.html", artist_=artist_)
