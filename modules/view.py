import sys

import PyInquirer.prompts

from modules.ctrla import DB, SongScraper
from modules.model import Album, Artist, Song


class CmdLnInterface:
    def __init__(self):
        self.db = DB()
        self.scrp = SongScraper()

        main_options = [{
            'type': 'list',
            'name': 'menu',
            'message': 'What do you want to do?',
            'choices': [
                "ARTISTS",
                "ALBUMS",
                "SONGS",
                "NEW",
                "LYRICS",
                "EXIT"
            ]
        }]
        while True:
            answer = PyInquirer.prompt(main_options)

            if answer["menu"] == "ARTISTS":
                self.artists_view()
            elif answer["menu"] == "ALBUMS":
                self.albums_view()
            elif answer["menu"] == "SONGS":
                self.songs_view()
            elif answer["menu"] == "NEW":
                self.fresh_view()
            elif answer["menu"] == "LYRICS":
                self.lyrics_view()
            elif answer["menu"] == "EXIT":
                sys.exit()

    def artists_view(self):
        """
        Functionality for managing Artists from the command line
        """
        self.print_list(self.db.get_all(Artist))

    def albums_view(self):
        """
        Functionality for managing Albums from the command line
        """
        self.print_list(self.db.get_all(Album))

    def songs_view(self):
        """
        Functionality for managing Songs from the command line
        """
        self.print_list(self.db.get_all(Song))

    def fresh_view(self):
        """
        Functionality for getting 'FRESH' music from r/HipHopHeads
        """
        self.print_list(self.scrp.get_fresh_music())

    def lyrics_view(self):
        """
        Functionality for getting lyrics from Genius.com
        """
        _ = "https://genius.com/Gorillaz-desole-lyrics"
        print(self.scrp.get_lyrics(_))

    @staticmethod
    def print_list(objects_list: list):
        """
        Print list of objects

        Args:
            objects_list(list): List of objects
        """
        for item in objects_list:
            item.to_string()
