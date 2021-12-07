import os

import dotenv

dotenv.load_dotenv()

GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")
SQLALCHEMY_DATABASE_URI = os.getenv("db_url")
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True

praw_client_id = os.getenv("client_id")
praw_client_secret = os.getenv("client_secret")
praw_username = os.getenv("username")
praw_password = os.getenv("password_")
praw_user_agent = os.getenv("user_agent")
