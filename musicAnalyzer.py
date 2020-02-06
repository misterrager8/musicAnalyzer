import sys
from model import *
from ctrla import *

albumCtrla = ctrla()
genres = ["Hip-Hop",
          "Soul / R&B",
          "Alternative",
          "Rock",
          "Soundtrack"]

if __name__ == "__main__":
  while True:

    answer = input(
"""
0 - View All Albums
1 - Add Album
2 - Delete Album
3 - Delete All
4 - Export
5 - Search
6 - Exit
""")

    if answer == 0:
      albumCtrla.viewAlbums()
    elif answer == 1:
      title = raw_input("Title? ")
      artist = raw_input("Artist? ")
      
      for idx, item in enumerate(genres):
        print(str(idx) + " - " + item)
      genre = input("Genre? ")
      
      releaseDate = raw_input("Release Date? (m/d/yyyy) ")
      try:
        rating = input("Rating? (1-5) ")
      except SyntaxError:
        rating = 0
        
      tags = raw_input("Tags? ")

      x = album(title, artist, genres[genre], releaseDate, rating, tags)
      albumCtrla.addAlbum(x)
      albumCtrla.viewAlbums()
    elif answer == 2:
      whichAlbum = input("Which Album? ")
      albumCtrla.deleteAlbum(whichAlbum)
      albumCtrla.viewAlbums()
    elif answer == 3:
      m = raw_input("Are you sure? ")
      if m == "Y" or m == "y":
        albumCtrla.deleteAllAlbums()
        albumCtrla.viewAlbums()
    elif answer == 4:
      albumCtrla.exportAlbums()
    elif answer == 5:
      j = raw_input("Search query: ")
      albumCtrla.searchAlbums(j)
    elif answer == 6:
      sys.exit()