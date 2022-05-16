from lyricsgenius import Genius
from praw import Reddit
from sqlalchemy import text

from musicAnalyzer import db


class Database:
    def __init__(self):
        pass

    @staticmethod
    def add(object_):
        db.session.add(object_)
        db.session.commit()

    @staticmethod
    def add_multiple(objects: list):
        for i in objects:
            db.session.add(i)
        db.session.commit()

    @staticmethod
    def get(type_, id_: int):
        return db.session.query(type_).get(id_)

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(object_):
        db.session.delete(object_)
        db.session.commit()

    @staticmethod
    def delete_multiple(objects: list):
        for i in objects:
            db.session.delete(i)
        db.session.commit()

    @staticmethod
    def search(type_, filter_: str = "", order_by: str = ""):
        return db.session.query(type_).filter(text(filter_)).order_by(text(order_by))

    @staticmethod
    def execute_stmt(stmt: str):
        db.session.execute(stmt)
        db.session.commit()


class GeniusWrapper(Genius):
    def __init__(self, **kwargs):
        super(GeniusWrapper, self).__init__(**kwargs)

    def get_news(self, per_page: int = 10) -> list:
        return self.latest_articles(per_page=per_page)["editorial_placements"]

    def get_charts(
        self,
        time_period: str = "week",
        genre: str = "all",
        per_page: int = 10,
        type_: str = "albums",
    ):
        return self.charts(
            time_period=time_period, chart_genre=genre, per_page=per_page, type_=type_
        )["chart_items"]


class RedditWrapper(Reddit):
    def __init__(self, **kwargs):
        super(RedditWrapper, self).__init__(**kwargs)

    def get_hot(self) -> list:
        return [
            i for i in self.subreddit("HipHopHeads").hot(limit=50) if not i.stickied
        ]

    def get_fresh(self) -> list:
        return [
            i for i in self.subreddit("HipHopHeads").hot(limit=50) if "FRESH" in i.title
        ]
