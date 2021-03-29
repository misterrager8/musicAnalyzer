from flask import render_template

from modules import app
from modules.ctrla import DB, SongScraper
from modules.model import Album, Artist, Song

music_db = DB()
y = SongScraper()

artists = music_db.get_all(Artist)
albums = music_db.get_all(Album)
songs = music_db.get_all(Song)

news = y.get_news()


@app.route("/")
def index():
    return render_template("index.html", fresh=news)


@app.route("/artists")
def artists_pg():
    return render_template("artists.html", artists=artists)


@app.route("/artist/<id_>")
def artists_profile_pg(id_: int):
    artist = music_db.find_by_id(Artist, id_)
    return render_template("artist_profile.html", artist=artist)


@app.route("/albums")
def albums_pg():
    return render_template("albums.html", albums=albums)


@app.route("/albums/sort-<sort_by>")
def sort(sort_by: str = "title"):
    g = {"title": sorted(albums, key=lambda x: x.title),
         "artist": sorted(albums, key=lambda x: x.artists.name),
         "year": sorted(albums, key=lambda x: x.release_date)}
    return render_template("albums.html", albums=g[sort_by])


@app.route("/albums/<id_>")
def album_profile_pg(id_: int):
    album = music_db.find_by_id(Album, id_)
    return render_template("album_profile.html", album=album)


@app.route("/songs")
def songs_pg():
    return render_template("songs.html", songs=songs)


@app.route("/songs/<id_>")
def song_profile_pg(id_: int):
    song = music_db.find_by_id(Song, id_)
    return render_template("song_profile.html", song=song)
