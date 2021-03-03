import os

import dotenv
import praw
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
        """
        Add object to DB
        Args:
            item: Item to be added to DB
        """
        db.session.add(item)
        db.session.commit()

    @staticmethod
    def insert_many(items: list):
        """
        Add multiple objects to the DB
        Args:
            items(list): Items in list to be added
        """
        db.session.add_all(items)
        db.session.commit()

    @staticmethod
    def get_all(item_type) -> list:
        """
        Get all objects of the specified Class, returns a list of them
        Args:
            item_type: type of Object to retrieve [Artist, Album, Song]
        Returns:
            list: List of all items of specified type
        """
        return db.session.query(item_type).all()

    @staticmethod
    def find_by_id(item_type, item_id: int) -> object:
        """
        Get a specific item of a specified type
        Args:
            item_type: type of Object to retrieve [Artist, Album, Song]
            item_id(int): the ID of the object being searched
        Returns:
            object: Specific item
        """
        return db.session.query(item_type).get(item_id)

    # @staticmethod
    # def update(stmt):
    #     pass

    @staticmethod
    def delete(item):
        """
        Delete a specific item from the DB
        Args:
            item: Object to be deleted
        """
        db.session.delete(item)
        db.session.commit()


class SongScraper:
    def __init__(self):
        self.reddit = praw.Reddit("bot1")

    def get_fresh_music(self) -> list:
        """
        Get posts with the tag 'FRESH' in r/HipHopHeads
        Returns:
            list: List of 'FRESH' posts
        """
        results = []
        for submission in self.reddit.subreddit("hiphopheads").new(limit=250):
            if "FRESH" in submission.title:
                results.append(submission.title)

        return results
