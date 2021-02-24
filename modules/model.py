import os

import dotenv
import sqlalchemy
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv()

db_host = os.getenv("host")
db_user = os.getenv("user")
db_passwd = os.getenv("passwd")
db_name = os.getenv("db")

engine = sqlalchemy.create_engine(f'mysql://{db_user}:{db_passwd}@{db_host}/{db_name}')
Base = declarative_base()

Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()


class Album(Base):
    __tablename__ = "albums"

    title = Column(Text)
    artist_id = Column(Integer) # FK
    genre = Column(Text)
    release_date = Column(Text)
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

    name = Column(Text)
    hometown = Column(Text)
    dob = Column(Text)
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

    name = Column(Text)
    artist_id = Column(Integer) # FK
    album_id = Column(Integer)  # FK
    play_count = Column(Integer)
    rating = Column(Integer)
    last_played = Column(Text)
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


Base.metadata.create_all(engine)
