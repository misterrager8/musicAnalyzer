import pymysql
from flask import Flask
from flask_login import LoginManager
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy

pymysql.install_as_MySQLdb()

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    login_manager.init_app(app)
    Scss(app, asset_dir="musicAnalyzer/static")

    with app.app_context():
        from musicAnalyzer.views.songs import songs
        from musicAnalyzer.views.artists import artists
        from musicAnalyzer.views.albums import albums
        from musicAnalyzer.views.tags import tags

        app.register_blueprint(songs)
        app.register_blueprint(albums)
        app.register_blueprint(artists)
        app.register_blueprint(tags)

        # db.drop_all()
        db.create_all()

        return app
