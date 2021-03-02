import os

import dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

dotenv.load_dotenv()
db_host = os.getenv("host")
db_user = os.getenv("user")
db_passwd = os.getenv("passwd")
db_name = os.getenv("db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{db_user}:{db_passwd}@{db_host}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class DB:
    def __init__(self):
        pass

    @staticmethod
    def insert_one(item: object):
        db.session.add(item)
        db.session.commit()

    @staticmethod
    def insert_many(items: list):
        db.session.add_all(items)
        db.session.commit()

    @staticmethod
    def get_all(item_type):
        return db.session.query(item_type).all()

    @staticmethod
    def find_by_id(item_type, item_id: int):
        return db.session.query(item_type).get(item_id)

    @staticmethod
    def update(stmt):
        pass

    @staticmethod
    def delete(item):
        db.session.delete(item)
        db.session.commit()
