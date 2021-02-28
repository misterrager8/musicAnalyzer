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
    def create(obj: object):
        db.session.add(obj)
        db.session.commit()

    @staticmethod
    def read(obj_name):
        return db.session.query(obj_name).all()

    @staticmethod
    def find_by_id(obj_name, obj_id: int):
        return db.session.query(obj_name).get(obj_id)

    @staticmethod
    def update(stmt):
        pass

    @staticmethod
    def delete(stmt):
        db.session.execute(stmt)
        db.session.commit()
        db.session.close()
