from sqlalchemy import Column, Integer, Text, ForeignKey, Date, text
from sqlalchemy.orm import relationship

from modules import db


class Artist(db.Model):
    __tablename__ = "artists"

    name = Column(Text)
    profile_pic = Column(Text)
    genius_id = Column(Text)
    id = Column(Integer, primary_key=True)
    albums = relationship("Album", backref="artists")
    songs = relationship("Song", backref="artists")

    def __init__(self, **kwargs):
        super(Artist, self).__init__(**kwargs)

    def __str__(self):
        return "%d\t%s" % (self.id, self.name)


class Album(db.Model):
    __tablename__ = "albums"

    title = Column(Text)
    artist = Column(Integer, ForeignKey("artists.id"))
    genre = Column(Text)
    release_date = Column(Date)
    rating = Column(Integer)
    cover_art = Column(Text)
    genius_id = Column(Text)
    id = Column(Integer, primary_key=True)
    songs = relationship("Song", backref="albums")

    def __init__(self, **kwargs):
        super(Album, self).__init__(**kwargs)

    def __str__(self):
        return "%d\t%s" % (self.id, self.title)


class Song(db.Model):
    __tablename__ = "songs"

    name = Column(Text)
    artist = Column(Integer, ForeignKey("artists.id"))
    album = Column(Integer, ForeignKey("albums.id"))
    track_num = Column(Integer)
    rating = Column(Integer)
    lyrics = Column(Text)
    genius_id = Column(Text)
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


class Database:
    def __init__(self):
        pass

    @staticmethod
    def create(object_):
        db.session.add(object_)
        db.session.commit()

    @staticmethod
    def get(type_, id_: int):
        return db.session.query(type_).get(id_)

    @staticmethod
    def delete(object_):
        db.session.delete(object_)
        db.session.commit()

    @staticmethod
    def search(type_, order_by: str = "", filter_: str = ""):
        return db.session.query(type_).order_by(text(order_by)).filter(text(filter_))

    @staticmethod
    def execute_stmt(stmt: str):
        db.session.execute(stmt)
        db.session.commit()
