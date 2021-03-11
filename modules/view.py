from flask import Flask, render_template

from modules.ctrla import DB
from modules.model import Album, Artist, Song

app = Flask(__name__)

b = DB().get_all(Artist)
c = DB().get_all(Album)
d = DB().get_all(Song)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/artists")
def artists_pg():
    return render_template("artists.html", artists=b)


@app.route("/albums")
def albums_pg():
    return render_template("albums.html", albums=c)


@app.route("/songs")
def songs_pg():
    return render_template("songs.html", songs=d)


if __name__ == "__main__":
    app.run(debug=True)
