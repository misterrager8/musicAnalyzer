import praw
from lyricsgenius import Genius

from modules.model import FreshItem


class RedditWrapper:
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


class GeniusWrapper:
    def __init__(self):
        self.genius = Genius()

    def search_artist(self, search_term: str):
        return self.genius.search_artist(search_term)
