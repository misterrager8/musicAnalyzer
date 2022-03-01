import os

import dotenv

dotenv.load_dotenv()

ENV = os.getenv("env")
SECRET_KEY = os.getenv("secret_key")
SQLALCHEMY_DATABASE_URI = os.getenv("db_url")
DEBUG = os.getenv("debug")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {"pool_recycle": 60}
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

praw_client_id = os.getenv("client_id")
praw_client_secret = os.getenv("client_secret")
praw_username = os.getenv("username")
praw_password = os.getenv("password_")
praw_user_agent = os.getenv("user_agent")
