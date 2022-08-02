from bs4 import BeautifulSoup
import requests


class Link:
    def __init__(self, url: str, title: str, source_name: str):
        self.url = url
        self.title = title
        self.source_name = source_name


def get_soup(url: str):
    return BeautifulSoup(requests.get(url).text, "html.parser")


def get_links():
    return (
        [
            Link(
                "http://www.hotnewhiphop.com" + i.get("href"),
                i.get_text(),
                "HotNewHipHop",
            )
            for i in get_soup("http://www.hotnewhiphop.com/").find_all(
                "a", class_="latestNews-title-anchor"
            )
        ]
        + [
            Link(i.find("a").get("href"), i.get_text(), "AllHipHop")
            for i in get_soup("http://allhiphop.com/news/").find_all(
                "h2", class_="entry-title"
            )
        ]
        + [
            Link(
                "http://hiphopdx.com" + i.find("a").get("href"),
                i.find("p").get_text(),
                "HipHopDX",
            )
            for i in get_soup("http://hiphopdx.com/news").find_all(
                "div", class_="text-wrap"
            )
        ]
    )
