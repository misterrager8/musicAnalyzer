import os

import dotenv

dotenv.load_dotenv()

ENV = os.getenv("env")
SECRET_KEY = os.getenv("secret_key")
SQLALCHEMY_DATABASE_URI = os.getenv("db_url")
DEBUG = os.getenv("debug")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {"pool_recycle": 60}
