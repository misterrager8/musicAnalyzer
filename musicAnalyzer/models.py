from musicAnalyzer import db
from flask_login import UserMixin
import markdown


class Artist:
    def __init__(self, genius_id: int, name: str, albums: list = []):
        self.genius_id = genius_id
        self.name = name
        self.albums = albums


class Album:
    def __init__(self, genius_id: int, title: str, songs: list = []):
        self.genius_id = genius_id
        self.title = title
        self.songs = songs


class Song:
    def __init__(self, genius_id: int, title: str):
        self.genius_id = genius_id
        self.title = title


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    role = db.Column(db.Text, default="user")
    blogs = db.relationship("Blog", backref="users", lazy="dynamic")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)


class NewsItem(db.Model):
    __tablename__ = "news"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)
    headline = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super(NewsItem, self).__init__(**kwargs)


class Blog(db.Model):
    __tablename__ = "blogs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text, default="")
    date_published = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, **kwargs):
        super(Blog, self).__init__(**kwargs)

    def get_markdown(self, **kwargs):
        return markdown.markdown(self.content)
