from flask import Flask, render_template

from modules.ctrla import DB, SongScraper
from modules.model import Album, Artist, Song

app = Flask(__name__)

x = DB()
y = SongScraper()

b = x.get_all(Artist)
c = x.get_all(Album)
d = x.get_all(Song)

e = y.get_news()


@app.route("/")
def index():
    return render_template("index.html", fresh=e)


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
