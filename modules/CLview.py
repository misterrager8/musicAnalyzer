from ctrla import *
from model import *

albumCtrla = ctrla()
genres = ["Hip-Hop/Rap",
          "R&B/Soul",
          "Alternative",
          "Rock",
          "Soundtrack"]

class homePrompts():
  def __init__(self):
    while True:
      self.printAlbums()
      answer = input(
"""
0 - View All Albums
1 - Add Album
2 - Delete Album
3 - Delete All
4 - Edit Album
5 - Export
6 - Import
7 - Search
8 - Exit
--------------------
""")

      if answer == 0:
        self.printAlbums()
      elif answer == 1:
        title = raw_input("Title? ")
        artist = raw_input("Artist? ")

        for idx, item in enumerate(genres):
          print(str(idx) + " - " + item)
        genre = input("------------\nGenre? ")

        releaseDate = raw_input("Release Date? (m/d/yyyy) ")
        try:
          rating = input("Rating? (1-5) ")
        except SyntaxError:
          rating = 0

        tags = raw_input("Tags? ")

        x = album(None, title, artist, genres[genre], releaseDate, rating, tags)
        albumCtrla.addAlbum(x)
      elif answer == 2:
        whichAlbum = input("Which Album? ")
        albumCtrla.deleteAlbum(whichAlbum)
      elif answer == 3:
        m = raw_input("Are you sure? ")
        if m == "Y" or m == "y":
          albumCtrla.deleteAllAlbums()
      elif answer == 4:
        whichAlbum = input("Which Album? ")
        searchType = input("0 - Change title | 1 - Change artist | 2 - Change release date | 3 - Change rating | 4 - Change tags\n")
        change = raw_input("Change? ")
        albumCtrla.editAlbum(whichAlbum, searchType, change)
      elif answer == 5:
        albumCtrla.exportAlbums()
      elif answer == 6:
        albumCtrla.importAlbums()
      elif answer == 7:
        searchType = input("0 - By title | 1 - By artist | 2 - By tags | 3 - By year\n")
        searchTerm = raw_input("Search query: ")
        r = albumCtrla.searchAlbums(searchTerm, searchType)
        print(str(len(r)) + " result(s) found.")
        for i in r:
          i.toString()
      elif answer == 8:
        sys.exit()

  def printAlbums(self):
    r = albumCtrla.viewAlbums()
    for obj in r:
      obj.toString()