from musicAnalyzer import db
from flask_login import UserMixin
import markdown


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text)
    password = db.Column(db.Text)
    role = db.Column(db.Text)
    date_created = db.Column(db.DateTime)
    blogs = db.relationship("Blog", backref="users")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)


class News(db.Model):
    __tablename__ = "news"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)
    headline = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super(News, self).__init__(**kwargs)


class Blog(db.Model):
    __tablename__ = "blogs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super(Blog, self).__init__(**kwargs)

    def get_content(self):
        return markdown.markdown(self.content)
