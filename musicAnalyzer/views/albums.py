from flask import Blueprint, render_template, request
from lyricsgenius import Genius
from musicAnalyzer.models import Album

genius = Genius()

albums = Blueprint("albums", __name__)


@albums.route("/albums", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("albums/albums.html")
    else:
        term = request.form["album"]
        return render_template(
            "albums/albums.html",
            results=genius.search_albums(term)["sections"][0]["hits"],
        )


@albums.route("/album")
def album():
    _ = genius.album(int(request.args.get("genius_id")))
    album_ = Album(
        _["album"]["id"],
        _["album"]["name"],
        genius.album_tracks(int(_["album"]["id"]))["tracks"],
    )
    return render_template("albums/album.html", album_=album_)
