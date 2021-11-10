from lyricsgenius import Genius
from sqlalchemy import Integer, Column, Text, ForeignKey, Date
from sqlalchemy.orm import relationship

from musicAnalyzer import db


class Artist(db.Model):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    genius_id = Column(Text)
    pic_url = Column(Text)
    albums = relationship("Album", backref="artists", lazy="dynamic")
    songs = relationship("Song", backref="artists", lazy="dynamic")

    def __init__(self, **kwargs):
        super(Artist, self).__init__(**kwargs)

    def get_albums(self):
        return Genius().artist_albums(self.genius_id)["albums"]


class Album(db.Model):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    release_date = Column(Date)
    genius_id = Column(Text)
    genre = Column(Text)
    cover_url = Column(Text)
    release_type = Column(Text)
    artist = Column(Integer, ForeignKey("artists.id"))
    songs = relationship("Song", backref="albums", lazy="dynamic")

    def __init__(self, **kwargs):
        super(Album, self).__init__(**kwargs)

    def get_songs(self):
        return Genius().album_tracks(self.genius_id)["tracks"]

    def get_release_type(self):
        if self.release_type == "Album":
            return [self.release_type, "#595cff"]
        elif self.release_type == "EP":
            return [self.release_type, "#00734e"]
        elif self.release_type == "Mixtape":
            return [self.release_type, "#e37424"]

    def get_avg_rating(self):
        return float(sum([i.rating for i in self.songs]) / self.songs.count())


class Song(db.Model):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    rating = Column(Integer, default=0)
    genius_url = Column(Text)
    track_num = Column(Integer)
    artist = Column(Integer, ForeignKey("artists.id"))
    album = Column(Integer, ForeignKey("albums.id"))

    def __init__(self, **kwargs):
        super(Song, self).__init__(**kwargs)


db.create_all()
