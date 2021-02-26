import sqlalchemy
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from modules.base import Base


class Artist(Base):
    __tablename__ = "artists"

    name = Column(Text)
    hometown = Column(Text)
    dob = Column(Text)
    id = Column(Integer, primary_key=True)
    albums = relationship("Album")

    def __init__(self,
                 name: str,
                 hometown: str = None,
                 dob: str = None,
                 artist_id: int = None):
        self.name = name
        self.hometown = hometown
        self.dob = dob
        self.artist_id = artist_id

    def to_string(self):
        print(self.name)


class Album(Base):
    __tablename__ = "albums"

    title = Column(Text)
    artist_id = Column(Integer, sqlalchemy.ForeignKey("artists.id"))
    genre = Column(Text)
    release_date = Column(Text)
    rating = Column(Integer)
    id = Column(Integer, primary_key=True)
    artist = relationship("Artist")

    def __init__(self,
                 title: str,
                 artist_id: int,
                 genre: str,
                 release_date: str = None,
                 rating: int = None,
                 album_id: int = None):
        self.title = title
        self.artist_id = artist_id
        self.genre = genre
        self.release_date = release_date
        self.rating = rating
        self.album_id = album_id

    def to_string(self):
        print(self.title)


class Song(Base):
    __tablename__ = "songs"

    name = Column(Text)
    artist_id = Column(Integer, sqlalchemy.ForeignKey("artists.id"))
    album_id = Column(Integer, sqlalchemy.ForeignKey("albums.id"))
    play_count = Column(Integer)
    rating = Column(Integer)
    last_played = Column(Text)
    id = Column(Integer, primary_key=True)

    def __init__(self,
                 name: str,
                 artist_id: int = None,
                 album_id: int = None,
                 play_count: int = None,
                 rating: int = None,
                 last_played: str = None,
                 song_id: int = None):
        self.name = name
        self.artist_id = artist_id
        self.album_id = album_id
        self.play_count = play_count
        self.rating = rating
        self.last_played = last_played
        self.song_id = song_id

    def to_string(self):
        print(self.name)
