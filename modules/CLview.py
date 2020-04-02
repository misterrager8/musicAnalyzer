from ctrla import *
from model import *

albumCtrla = Ctrla()
genres = ["Hip-Hop/Rap",
          "R&B/Soul",
          "Alternative",
          "Rock",
          "Soundtrack"]
mainOptions = ["View All",
               "Add Album",
               "Delete Album",
               "Delete All",
               "Edit Album",
               "Export",
               "Import",
               "Search",
               "Exit"]


class HomePrompts:
    def __init__(self):
        while True:
            self.print_albums()
            self.print_options(mainOptions)
            answer = input("What do you want to do? ")

            if mainOptions[answer] == "View All":
                self.print_albums()
            elif mainOptions[answer] == "Add Album":
                title = raw_input("Title? ")
                artist = raw_input("Artist? ")

                self.print_options(genres)
                genre = input("Genre? ")
                release_date = raw_input("Release Date? (m/d/yyyy) ")

                try:
                    # TODO: rating is rounding up/down on input, needs fix
                    rating = input("Rating? (1-5) ")
                except SyntaxError:
                    rating = 0

                tags = raw_input("Tags? ")

                x = Album(None, title, artist, genres[genre], release_date, rating, tags)
                albumCtrla.add_album(x)

            elif mainOptions[answer] == "Delete Album":
                which_album = input("Which Album? ")
                albumCtrla.delete_album(which_album)

            elif mainOptions[answer] == "Delete All":
                m = raw_input("Are you sure? ")
                if m == "Y" or m == "y":
                    albumCtrla.delete_all_albums()
            elif mainOptions[answer] == "Edit Album":
                which_album = input("Which Album? ")
                search_type = input(
                    "0 - Change title | 1 - Change artist | 2 - Change release date | 3 - Change rating | 4 - Change "
                    "tags\n")
                change = raw_input("Change? ")
                albumCtrla.edit_album(which_album, search_type, change)
            elif mainOptions[answer] == "Export":
                albumCtrla.export_albums()
            elif mainOptions[answer] == "Import":
                albumCtrla.import_albums()
            elif mainOptions[answer] == "Search":
                search_type = input("0 - By title | 1 - By artist | 2 - By tags | 3 - By year\n")
                search_term = raw_input("Search query: ")
                r = albumCtrla.search_albums(search_term, search_type)
                print(str(len(r)) + " result(s) found.")
                for i in r:
                    i.to_string()
            elif mainOptions[answer] == "Exit":
                sys.exit()

    @classmethod
    def print_options(cls, ls):
        for idx, i in enumerate(ls):
            print(str(idx) + " - " + i)

    @classmethod
    def print_albums(cls):
        r = albumCtrla.view_albums()
        for obj in r:
            obj.to_string()
