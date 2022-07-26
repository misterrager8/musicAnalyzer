from bs4 import BeautifulSoup
import requests


class Link:
    def __init__(self, url: str, domain_name: str, title: str):
        self.url = url
        self.domain_name = domain_name
        self.title = title


def get_links():
    return [
        Link("https://www.hotnewhiphop.com" + i.get("href"), "HotNewHipHop", i.text)
        for i in BeautifulSoup(
            requests.get("https://www.hotnewhiphop.com").content, "html.parser"
        ).find_all("a", class_="latestNews-title-anchor")
    ] + [
        Link(i.get("href"), "AllHipHop", i.find("h2").text)
        for i in BeautifulSoup(
            requests.get("https://allhiphop.com/").content, "html.parser"
        ).find_all("a", class_="entry-box-horizontal")
    ]
