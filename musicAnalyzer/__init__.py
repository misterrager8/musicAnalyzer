from flask import Flask
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

pymysql.install_as_MySQLdb()


db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from musicAnalyzer.views.artists import artists
        from musicAnalyzer.views.albums import albums
        from musicAnalyzer.views.songs import songs
        from musicAnalyzer.views.blogs import blogs
        from musicAnalyzer.views.news import news

        app.register_blueprint(artists)
        app.register_blueprint(albums)
        app.register_blueprint(songs)
        app.register_blueprint(blogs)
        app.register_blueprint(news)

        db.create_all()

        return app
