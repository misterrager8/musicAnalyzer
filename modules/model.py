from datetime import datetime

from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from modules import db


class Artist(db.Model):
    __tablename__ = "artists"

    name = Column(Text)
    hometown = Column(Text)
    dob = Column(Text)
    id = Column(Integer, primary_key=True)
    albums = relationship("Album", backref="artists")
    songs = relationship("Song", backref="artists")

    def __init__(self, name: str):
        """
        Create Artist object

        Args:
            name(str): Name of the Artist
        """
        self.name = name

    def add_albums(self, new_albums: list):
        """
        Add a list of Albums to the Artist

        Args:
            new_albums (list): List of Albums to be added
        """
        for i in new_albums:
            self.albums.append(i)

        db.session.commit()

    def duplicate_checked(self):
        """
        Checks whether Artist is already in DB

        Returns:
            Artist: Either new Artist or preexisting Artist
        """
        _ = db.session.query(Artist).filter(Artist.name == self.name).first()
        if _ is not None:
            return _
        else:
            return self

    def to_string(self):
        print(str(self.id) + "\t" + self.name)


class Album(db.Model):
    __tablename__ = "albums"

    title = Column(Text)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    genre = Column(Text)
    release_date = Column(Text)
    rating = Column(Integer)
    id = Column(Integer, primary_key=True)
    songs = relationship("Song", backref="albums")

    def __init__(self,
                 title: str,
                 artist_id=None,
                 genre: str = None,
                 release_date: str = None,
                 rating=None):
        """
        Create Album object

        Args:
            title(str): title of the Album
        """
        self.title = title
        self.artist_id = artist_id
        self.genre = genre
        self.release_date = release_date
        self.rating = rating

    def add_songs(self, new_songs: list):
        """
        Add Songs to the Album

        Args:
            new_songs(list): List of Songs to be added to the Album
        """
        for i in new_songs:
            i.artists = self.artists
            self.songs.append(i)

        db.session.commit()

    def to_string(self):
        print(str(self.id) + "\t" + self.title)


class Song(db.Model):
    __tablename__ = "songs"

    name = Column(Text)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    album_id = Column(Integer, ForeignKey("albums.id"))
    play_count = Column(Integer)
    rating = Column(Integer)
    last_played = Column(Text)
    id = Column(Integer, primary_key=True)

    def __init__(self, name: str):
        """
        Create Song object

        Args:
            name(str): Name of the Song
        """
        self.name = name

    def to_string(self):
        print(str(self.id) + "\t" + self.name)


class FreshItem(db.Model):
    __tablename__ = "fresh_items"

    title = Column(Text)
    url = Column(Text)
    time_posted = Column(Text)
    id = Column(Integer, primary_key=True)

    def __init__(self,
                 title: str,
                 url: str,
                 time_posted: str):
        """
        'FRESH' Submission object from PRAW

        Args:
            title (str): Title of the Submission
            url (str): URL of the Submission
            time_posted (str): Time posted of the Submission in UTC
        """
        self.title = title
        self.url = url
        self.time_posted = datetime.utcfromtimestamp(float(time_posted))

    def to_string(self):
        print(str(self.time_posted) + "\t" + self.title)


db.create_all()
