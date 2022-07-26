import dotenv
import os

dotenv.load_dotenv()

ENV = os.getenv("env")
DEBUG = os.getenv("debug")
SQLALCHEMY_DATABASE_URI = os.getenv("sqlalchemy_database_uri")
SECRET_KEY = os.getenv("secret_key")
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")
SQLALCHEMY_TRACK_MODIFICATIONS = False

PRAW_CLIENT_ID = os.getenv("client_id")
PRAW_CLIENT_SECRET = os.getenv("client_secret")
PRAW_USERNAME = os.getenv("username")
PRAW_PASSWORD = os.getenv("password_")
PRAW_USER_AGENT = os.getenv("user_agent")
