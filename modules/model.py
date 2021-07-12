from datetime import datetime

from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from modules import db


class Artist(db.Model):
    __tablename__ = "artists"

    name = Column(Text)
    hometown = Column(Text)
    dob = Column(Text)
    profile_pic = Column(Text)
    wiki_id = Column(Text)
    id = Column(Integer, primary_key=True)
    albums = relationship("Album", backref="artists")
    songs = relationship("Song", backref="artists")

    def __init__(self, **kwargs):
        super(Artist, self).__init__(**kwargs)

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
    wiki_id = Column(Text)
    genius_url = Column(Text)
    id = Column(Integer, primary_key=True)
    songs = relationship("Song", backref="albums")

    def __init__(self, **kwargs):
        super(Album, self).__init__(**kwargs)

    def __str__(self):
        return "%d\t%s" % (self.id, self.title)


class Song(db.Model):
    __tablename__ = "songs"

    name = Column(Text)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    album_id = Column(Integer, ForeignKey("albums.id"))
    play_count = Column(Integer)
    track_num = Column(Integer, default=0)
    rating = Column(Integer)
    last_played = Column(Text)
    lyrics = Column(Text)
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Song, self).__init__(**kwargs)

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
