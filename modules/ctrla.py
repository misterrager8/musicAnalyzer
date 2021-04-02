import bs4
import praw
import requests

from modules import db
from modules.model import FreshItem


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
    def get_all(item_type, order_by=None):
        """
        Get all objects of the specified Class, returns a list of them

        Args:
            item_type: type of Object to retrieve [Artist, Album, Song]
            order_by: sorting criteria
        Returns:
            List of all items of specified type
        """
        return db.session.query(item_type).order_by(order_by)

    @staticmethod
    def find_by_id(item_type, item_id: int):
        """
        Get a specific item of a specified type

        Args:
            item_type: type of Object to retrieve [Artist, Album, Song]
            item_id(int): the ID of the object being searched
        Returns:
            Specific item
        """
        return db.session.query(item_type).get(item_id)

    @staticmethod
    def search(item_type, search_term):
        _ = "%{}%".format(search_term)
        results = db.session.query(item_type).filter(item_type.like(_)).all()
        return results

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

    def get_news(self) -> list:
        """
        Get posts in r/HipHopHeads

        Returns:
            list: List of posts
        """
        results = []
        for submission in self.reddit.subreddit("hiphopheads").hot(limit=25):
            _ = FreshItem(submission.title,
                          submission.url,
                          submission.created_utc)
            results.append(_)

        return results

    def get_fresh(self) -> list:
        """
        Get posts with the tag 'FRESH' in r/HipHopHeads

        Returns:
            list: List of 'FRESH' posts
        """
        results = []
        for submission in self.reddit.subreddit("hiphopheads").new(limit=250):
            if "FRESH" in submission.title:
                _ = FreshItem(submission.title,
                              submission.url,
                              submission.created_utc)
                results.append(_)

        return results

    @staticmethod
    def get_lyrics(genius_url: str) -> str:
        """
        Get lyrics of a song from Genius.com

        Args:
            genius_url (str): Genius URL of the lyrics

        Returns:
            str: The lyrics of the song
        """
        page = requests.get(genius_url)
        soup = bs4.BeautifulSoup(page.content, 'html.parser')
        x = soup.find_all("div", class_="lyrics")

        return x[0].find("p").text

    @staticmethod
    def search_lyrics(search_term: str):
        page = requests.get("https://genius.com/search?q=" + search_term)
        soup = bs4.BeautifulSoup(page.content, 'html.parser')
        print(page.content)
        _ = soup.find_all("div", class_="mini_card-title")
