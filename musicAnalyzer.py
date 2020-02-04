import sys
from model import *
from ctrla import *

albumCtrla = ctrla()

if __name__ == "__main__":
  while True:
    albumCtrla.viewAlbums()

    answer = input(
"""
1 - Add Album
2 - Delete Album
3 - Delete All
4 - Export
5 - Exit
""")

    if answer == 1:
      title = raw_input("Title? ")
      artist = raw_input("Artist? ")
      genre = raw_input("Genre? ")
      releaseDate = raw_input("Release Date? (m/d/yyyy) ")
      rating = input("Rating? (1-5) ")
      tags = raw_input("Tags? ")

      x = album(title, artist, genre, releaseDate, rating, tags)
      albumCtrla.addAlbum(x)
    elif answer == 2:
      whichAlbum = input("Which Album? ")
      albumCtrla.deleteAlbum(whichAlbum)
    elif answer == 3:
      m = raw_input("Are you sure? ")
      if m == "Y" or m == "y":
        albumCtrla.deleteAllAlbums()
    elif answer == 4:
      albumCtrla.exportAlbums()
    elif answer == 5:
      sys.exit()