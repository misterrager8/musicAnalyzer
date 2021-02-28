import sqlalchemy
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from modules.ctrla import db


class Artist(db.Model):
    __tablename__ = "artists"

    name = Column(Text)
    hometown = Column(Text)
    dob = Column(Text)
    id = Column(Integer, primary_key=True)
    albums = relationship("Album", backref="artists")

    def __init__(self, name: str):
        self.name = name

    def to_string(self):
        print(self.name)


class Album(db.Model):
    __tablename__ = "albums"

    title = Column(Text)
    artist_id = Column(Integer, sqlalchemy.ForeignKey("artists.id"))
    genre = Column(Text)
    release_date = Column(Text)
    rating = Column(Integer)
    id = Column(Integer, primary_key=True)
    songs = relationship("Song", backref="albums")

    def __init__(self, title: str):
        self.title = title

    def to_string(self):
        print([self.title])


class Song(db.Model):
    __tablename__ = "songs"

    name = Column(Text)
    artist_id = Column(Integer, sqlalchemy.ForeignKey("artists.id"))
    album_id = Column(Integer, sqlalchemy.ForeignKey("albums.id"))
    play_count = Column(Integer)
    rating = Column(Integer)
    last_played = Column(Text)
    id = Column(Integer, primary_key=True)

    def __init__(self, name: str):
        self.name = name

    def to_string(self):
        print(self.name)


db.create_all()
