import os
import shutil

import bs4
import praw
import requests
from wikipedia import wikipedia

from modules import db
from modules.model import FreshItem, Album, Artist, Song


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


class WikiScraper:
    def __init__(self):
        pass

    @staticmethod
    def get_tracklist(album: Album):
        page = requests.get(album.wiki_url)
        soup = bs4.BeautifulSoup(page.content, "html.parser")
        _ = []
        table = soup.find("table", class_="tracklist")
        for i in table.tbody.find_all("tr")[1:-1]:
            h = i.contents[1]
            if h.contents[0].string == "\"":
                _.append(Song(h.contents[1].string))
            else:
                _.append(Song(h.contents[0].string.strip("\" ")))

        album.add_songs(_)

    @staticmethod
    def get_cover_art(album: Album):
        _ = wikipedia.WikipediaPage(pageid=album.wiki_id).images
        for idx, i in enumerate(_): print("%d\t%s" % (idx, i))
        choice = input("? ")
        image_url = _[int(choice)]

        filename = image_url.split("/")[-1]
        ext = os.path.splitext(filename)[1]

        r = requests.get(image_url, stream=True)

        r.raw.decode_content = True

        img_path = os.path.join(os.path.dirname(__file__), "../modules/static/")

        with open(img_path + filename, "wb") as f:
            shutil.copyfileobj(r.raw, f)

        old_name = img_path + filename
        new_name = img_path + album.title + ext
        os.rename(old_name, new_name)

        album.set_cover_art(album.title + ext)

    @staticmethod
    def get_artist_pic(artist: Artist):
        _ = wikipedia.WikipediaPage(pageid=artist.wiki_id).images
        for idx, i in enumerate(_): print("%d\t%s" % (idx, i))
        choice = input("? ")
        image_url = _[int(choice)]

        filename = image_url.split("/")[-1]
        ext = os.path.splitext(filename)[1]

        r = requests.get(image_url, stream=True)

        r.raw.decode_content = True

        img_path = os.path.join(os.path.dirname(__file__), "../modules/static/")

        with open(img_path + filename, "wb") as f:
            shutil.copyfileobj(r.raw, f)

        old_name = img_path + filename
        new_name = img_path + artist.name + ext
        os.rename(old_name, new_name)

        artist.set_pic(artist.name + ext)

    @staticmethod
    def get_lyrics(genius_url: str):
        init_url = genius_url
        album_name = init_url.split("/")[5]

        res_a = requests.get(init_url)
        os.makedirs("/" + album_name, 0o777)

        soup_a = bs4.BeautifulSoup(res_a.text, features="html.parser")
        type(soup_a)

        elems_a = soup_a.findAll("a", {"class": "u-display_block", "href": True})

        for i, item in enumerate(elems_a):
            res = requests.get(item["href"])

            soup = bs4.BeautifulSoup(res.text, features="html.parser")
            type(soup)

            return soup.select(".lyrics")[0].getText()
