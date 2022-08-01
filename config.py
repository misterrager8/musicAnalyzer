import dotenv
import os

dotenv.load_dotenv()

DEBUG = os.getenv("debug")
ENV = os.getenv("env")
SQLALCHEMY_DATABASE_URI = os.getenv("sqlalchemy_database_uri")
SECRET_KEY = os.getenv("secret_key")
SQLALCHEMY_ENGINE_OPTIONS = {"pool_recycle": 60}
SQLALCHEMY_TRACK_MODIFICATIONS = False
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

CLIENT_ID = os.getenv("client_id")
CLIENT_SECRET = os.getenv("client_secret")
USERNAME = os.getenv("username")
PASSWORD_ = os.getenv("password_")
USER_AGENT = os.getenv("user_agent")
