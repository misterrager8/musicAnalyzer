from flask import render_template, request

from modules import app, db
from modules.ctrla import DB, SongScraper
from modules.model import Album, Artist, Song

music_db = DB()
y = SongScraper()

albums = music_db.get_all(Album)
songs = music_db.get_all(Song)

news = y.get_news()


def refresh(item_type):
    for i in music_db.get_all(item_type): db.session.refresh(i)


@app.route("/")
def index():
    return render_template("index.html", fresh=news)


@app.route("/artists")
def artists_pg():
    artists = music_db.get_all(Artist)
    return render_template("artists.html", artists=sorted(artists, key=lambda x: x.name))


@app.route("/artist/<id_>")
def artists_profile_pg(id_: int):
    artist = music_db.find_by_id(Artist, id_)
    return render_template("artist_profile.html", artist=artist)


@app.route("/albums")
def albums_pg():
    j = music_db.get_all_paginate(Album)
    return render_template("albums.html", albums=j)


@app.route("/albums/sort-<sort_by>")
def sort_albums(sort_by: str):
    _ = {"title": sorted(albums, key=lambda x: x.title),
         "artist": sorted(albums, key=lambda x: x.artists.name),
         "year": sorted(albums, key=lambda x: x.release_date, reverse=True)}
    return render_template("albums.html", albums=_[sort_by], sort_by=sort_by)


@app.route("/albums/<id_>")
def album_profile_pg(id_: int):
    album = music_db.find_by_id(Album, id_)
    _ = sorted(album.songs, key=lambda x: x.track_num)
    return render_template("album_profile.html", album=album, tracks=_)


@app.route("/songs")
def songs_pg():
    return render_template("songs.html", songs=sorted(songs, key=lambda x: x.name))


@app.route("/songs/<id_>")
def song_profile_pg(id_: int):
    song = music_db.find_by_id(Song, id_)
    return render_template("song_profile.html", song=song)


@app.route("/search", methods=["POST"])
def results_pg():
    if request.method == "POST":
        search_term = request.form["search_term"]
        results = {"artist_results": music_db.search(Artist.name, search_term),
                   "album_results": music_db.search(Album.title, search_term),
                   "song_results": music_db.search(Song.name, search_term)}
        return render_template("results.html", search_term=search_term, results=results)


@app.route("/add", methods=["GET", "POST"])
def add_pg():
    if request.method == "POST":
        _ = Artist(request.form["artist_name"])
        music_db.insert_one(_)
        render_template("artists.html")

    return render_template("add.html")


@app.route("/edit<id_>", methods=["POST"])
def edit(id_: int):
    if request.method == "POST":
        artist = music_db.find_by_id(Artist, id_)
        _ = Album(request.form["album_title"], release_date=request.form["year"])
        artist.add_albums([_])
        refresh(Artist)
        return render_template("artist_profile.html", artist=artist)
