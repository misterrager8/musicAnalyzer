import os
from datetime import datetime

import dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

dotenv.load_dotenv()

db_host = os.getenv("host")
db_user = os.getenv("user")
db_passwd = os.getenv("passwd")
db_name = os.getenv("db")
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{db_user}:{db_passwd}@{db_host}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


def get_time_posted(date_):
    return datetime.utcfromtimestamp(float(date_)).strftime("%B %-d, %Y %I:%M %p")


app.jinja_env.globals.update(get_time_posted=get_time_posted)
