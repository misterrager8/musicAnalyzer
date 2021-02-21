from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Album(Base):
    __tablename__ = "albums"

    title = Column(String)
    artist_id = Column(Integer)  # FK
    genre = Column(String)
    release_date = Column(String)
    rating = Column(Integer)
    album_id = Column(Integer, primary_key=True)

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


class Artist(Base):
    __tablename__ = "artists"

    name = Column(String)
    hometown = Column(String)
    dob = Column(String)
    artist_id = Column(Integer, primary_key=True)

    def __init__(self,
                 name: str,
                 hometown: str = None,
                 dob: str = None,
                 artist_id: int = None):
        self.name = name
        self.hometown = hometown
        self.dob = dob
        self.artist_id = artist_id


class Song(Base):
    __tablename__ = "songs"

    name = Column(String)
    artist_id = Column(Integer)  # FK
    album_id = Column(Integer)  # FK
    play_count = Column(Integer)
    rating = Column(Integer)
    last_played = Column(String)
    song_id = Column(Integer, primary_key=True)

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
