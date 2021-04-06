import os
from datetime import datetime

import bs4
import requests
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from modules import db


class Artist(db.Model):
    __tablename__ = "artists"

    name = Column(Text)
    hometown = Column(Text)
    dob = Column(Text)
    profile_pic = Column(Text)
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

    def add_songs(self, new_songs: list):
        """
        Add a list of Songs to the Artist

        Args:
            new_songs (list): List of Songs to be added
        """
        for i in new_songs:
            self.songs.append(i)

        db.session.commit()

    def set_pic(self, filename: str):
        pics_dir = os.path.join(os.path.dirname(__file__), "static/")

        og_filename = os.path.join(pics_dir, filename)
        new_filename = os.path.join(pics_dir, "%s.jpg" % self.name)

        os.rename(og_filename, new_filename)

        self.profile_pic = "%s.jpg" % self.name
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

    def __str__(self):
        return "%d\t%s" % (self.id, self.name)


class Album(db.Model):
    __tablename__ = "albums"

    title = Column(Text)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    genre = Column(Text)
    release_date = Column(Text)
    rating = Column(Integer)
    cover_art = Column(Text)
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

    def set_cover_art(self, filename):
        pics_dir = os.path.join(os.path.dirname(__file__), "static/")

        og_filename = os.path.join(pics_dir, filename)
        new_filename = os.path.join(pics_dir, "%s.jpg" % self.title)

        os.rename(og_filename, new_filename)

        self.cover_art = "%s.jpg" % self.title
        db.session.commit()

    def __str__(self):
        return "%d\t%s" % (self.id, self.title)


class Song(db.Model):
    __tablename__ = "songs"

    name = Column(Text)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    album_id = Column(Integer, ForeignKey("albums.id"))
    play_count = Column(Integer)
    track_num = Column(Integer)
    rating = Column(Integer)
    last_played = Column(Text)
    lyrics = Column(Text)
    id = Column(Integer, primary_key=True)

    def __init__(self, name: str):
        """
        Create Song object

        Args:
            name(str): Name of the Song
        """
        self.name = name

    def add_lyrics(self, genius_url: str):
        """
        Get lyrics of a song from Genius.com

        Args:
            genius_url (str): Genius URL of the lyrics
        """
        page = requests.get(genius_url)
        soup = bs4.BeautifulSoup(page.content, 'html.parser')
        x = soup.find_all("div", class_="lyrics")

        self.lyrics = x[0].find("p").text
        db.session.commit()

    def __str__(self):
        return "%d\t%s" % (self.id, self.name)


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

    def __str__(self):
        return "%s\t%s" % (self.time_posted, self.title)


db.create_all()
