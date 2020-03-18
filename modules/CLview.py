from ctrla import *
from model import *

albumCtrla = ctrla()
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

class homePrompts():
  def __init__(self):
    while True:
      self.printAlbums()
      self.printOptions(mainOptions)
      answer = input("What do you want to do? ")

      if mainOptions[answer] == "View All":
        self.printAlbums()
      elif mainOptions[answer] == "Add Album":
        title = raw_input("Title? ")
        artist = raw_input("Artist? ")

        self.printOptions(genres)
        genre = input("Genre? ")
        releaseDate = raw_input("Release Date? (m/d/yyyy) ")
        
        try:
          #TODO: rating is rounding up/down on input, needs fix
          rating = input("Rating? (1-5) ")
        except SyntaxError:
          rating = 0

        tags = raw_input("Tags? ")

        x = album(None, title, artist, genres[genre], releaseDate, rating, tags)
        albumCtrla.addAlbum(x)
        
      elif mainOptions[answer] == "Delete Album":
        whichAlbum = input("Which Album? ")
        albumCtrla.deleteAlbum(whichAlbum)
        
      elif mainOptions[answer] == "Delete All":
        m = raw_input("Are you sure? ")
        if m == "Y" or m == "y":
          albumCtrla.deleteAllAlbums()
      elif mainOptions[answer] == "Edit Album":
        whichAlbum = input("Which Album? ")
        searchType = input("0 - Change title | 1 - Change artist | 2 - Change release date | 3 - Change rating | 4 - Change tags\n")
        change = raw_input("Change? ")
        albumCtrla.editAlbum(whichAlbum, searchType, change)
      elif mainOptions[answer] == "Export":
        albumCtrla.exportAlbums()
      elif mainOptions[answer] == "Import":
        albumCtrla.importAlbums()
      elif mainOptions[answer] == "Search":
        searchType = input("0 - By title | 1 - By artist | 2 - By tags | 3 - By year\n")
        searchTerm = raw_input("Search query: ")
        r = albumCtrla.searchAlbums(searchTerm, searchType)
        print(str(len(r)) + " result(s) found.")
        for i in r:
          i.toString()
      elif mainOptions[answer] == "Exit":
        sys.exit()
        
  def printOptions(self, ls):
    for idx, i in enumerate(ls):
      print(str(idx) + " - " + i)

  def printAlbums(self):
    r = albumCtrla.viewAlbums()
    for obj in r:
      obj.toString()