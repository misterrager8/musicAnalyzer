from flask_login import UserMixin
from sqlalchemy import Column, Integer, Text, ForeignKey, Date, text
from sqlalchemy.orm import relationship

from musicAnalyzer import db


class AlbumTag(db.Model):
    __tablename__ = "albumtags"

    id = Column(Integer, primary_key=True)
    album_id = Column(Integer, ForeignKey("albums.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))

    def __init__(self, **kwargs):
        super(AlbumTag, self).__init__(**kwargs)

    def get_tag(self):
        return Tag.query.filter(Tag.id == self.tag_id).first()

    def get_album(self):
        return Album.query.filter(Album.id == self.album_id).first()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(Text)
    password = Column(Text)
    tags = relationship("Tag", backref="users", lazy="dynamic")
    artists = relationship("Artist", backref="users", lazy="dynamic")
    albums = relationship("Album", backref="users", lazy="dynamic")
    songs = relationship("Song", backref="users", lazy="dynamic")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def get_artists(self, filter_: str = "", order_by: str = "id desc"):
        return self.artists.filter(text(filter_)).order_by(text(order_by))

    def get_albums(self, filter_: str = "", order_by: str = "release_date desc"):
        return self.albums.filter(text(filter_)).order_by(text(order_by))

    def get_songs(self, filter_: str = "", order_by: str = "name"):
        return self.songs.filter(text(filter_)).order_by(text(order_by))


class Artist(db.Model):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    albums = relationship("Album", backref="artists", lazy="dynamic")
    songs = relationship("Song", backref="artists", lazy="dynamic")
    user_id = Column(Integer, ForeignKey("users.id"))

    def __init__(self, **kwargs):
        super(Artist, self).__init__(**kwargs)

    def get_albums(self, filter_: str = "", order_by: str = "release_date desc"):
        return self.albums.filter(text(filter_)).order_by(text(order_by))

    def get_songs(self, filter_: str = "", order_by: str = "name"):
        return self.songs.filter(text(filter_)).order_by(text(order_by))


class Album(db.Model):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    release_date = Column(Date)
    release_type = Column(Text)
    genre = Column(Text)
    songs = relationship("Song", backref="albums", lazy="dynamic")
    artist_id = Column(Integer, ForeignKey("artists.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    def __init__(self, **kwargs):
        super(Album, self).__init__(**kwargs)

    def get_songs(self, filter_: str = "", order_by: str = "track_num"):
        return self.songs.filter(text(filter_)).order_by(text(order_by))

    def get_tags(self):
        results = []
        for i in AlbumTag.query.filter(AlbumTag.album_id == self.id):
            _: AlbumTag = AlbumTag.query.get(i.id)
            results.append(_)
        return results

    def get_avg_rating(self):
        rated_songs = [i.rating for i in self.songs if i.rating > 0]
        return "%.2f" % float(sum(rated_songs) / len(rated_songs)) if rated_songs else None


class Song(db.Model):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    rating = Column(Integer, default=0)
    track_num = Column(Integer)
    plays = Column(Integer, default=0)
    album_id = Column(Integer, ForeignKey("albums.id"))
    artist_id = Column(Integer, ForeignKey("artists.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    def __init__(self, **kwargs):
        super(Song, self).__init__(**kwargs)


class Tag(db.Model):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    color = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))

    def __init__(self, **kwargs):
        super(Tag, self).__init__(**kwargs)

    def get_albums(self):
        results = []
        for i in AlbumTag.query.filter(AlbumTag.tag_id == self.id):
            _: Album = db.session.query(Album).get(i.album_id)
            results.append(_)
        return results
