import sys

import PyInquirer.prompts

from modules.ctrla import DB
from modules.model import Album, Artist, Song


class CmdLnInterface:
    def __init__(self):
        self.db = DB()

        main_options = [{
            'type': 'list',
            'name': 'menu',
            'message': 'What do you want to do?',
            'choices': [
                "ARTISTS",
                "ALBUMS",
                "SONGS",
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

    @staticmethod
    def print_list(objects_list: list):
        """
        Print list of objects
        Args:
            objects_list(list): List of objects
        """
        for item in objects_list:
            item.to_string()
