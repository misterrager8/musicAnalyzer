import pymysql
from flask_admin.contrib.sqla import ModelView
from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

pymysql.install_as_MySQLdb()

db = SQLAlchemy()
login_manager = LoginManager()
admin = Admin()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)

    with app.app_context():
        from musicAnalyzer.views.songs import songs
        from musicAnalyzer.views.artists import artists
        from musicAnalyzer.views.albums import albums
        from musicAnalyzer.views.tags import tags
        from musicAnalyzer.models import User

        app.register_blueprint(songs)
        app.register_blueprint(albums)
        app.register_blueprint(artists)
        app.register_blueprint(tags)

        admin.add_view(ModelView(User, db.session))

        # db.drop_all()
        db.create_all()

        return app
