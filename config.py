import os

import dotenv

dotenv.load_dotenv()

host = os.getenv("host")
user = os.getenv("user")
password = os.getenv("password")
db_name = os.getenv("db_name")
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

SQLALCHEMY_DATABASE_URI = f"mysql://{user}:{password}@{host}/{db_name}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
