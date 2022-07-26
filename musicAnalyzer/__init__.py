from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import pymysql


pymysql.install_as_MySQLdb()


db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from . import views
        from .views.news import news
        from .views.blogs import blogs
        from .views.artists import artists

        app.register_blueprint(news)
        app.register_blueprint(blogs)
        app.register_blueprint(artists)

        db.create_all()

        return app
