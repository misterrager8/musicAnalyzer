from flask import Blueprint, render_template, request
from lyricsgenius import Genius

genius = Genius()
songs = Blueprint("songs", __name__)


@songs.route("/songs", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("songs/songs.html")
    else:
        term = request.form["song"]
        return render_template(
            "songs/songs.html",
            results=genius.search_songs(term)["hits"],
        )


@songs.route("/song")
def song():
    genius_id = request.args.get("genius_id")
    return render_template(
        "songs/song.html", song_=genius.search_song(song_id=genius_id)
    )
