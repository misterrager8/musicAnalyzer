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
        return self.name


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
        return "%s,%s,%s,%s" % (self.title, self.artists.name, self.genre, self.release_date)


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
        return "%s,%s,%s" % (self.name, self.artists.name, self.albums.title)


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
