import sys
from model import *
from ctrla import *

albumCtrla = ctrla()

while True:
  albumCtrla.viewAlbums()
  
  answer = input("""1 - Add Album
2 - Delete Album
3 - Delete All
4 - Exit
""")

  if answer == 1:
    title = raw_input("Title? ")
    artist = raw_input("Artist? ")
    genre = raw_input("Genre? ")
    releaseDate = raw_input("Release Date? ")
    rating = input("Rating? ")
    tags = raw_input("Tags? ")
    
    x = album(title, artist, genre, releaseDate, rating, tags)
    albumCtrla.addAlbum(x)
  elif answer == 2:
    print("remalbum")
  elif answer == 3:
    m = raw_input("Are you sure? ")
    if m == "Y":
      albumCtrla.deleteAllAlbums()
  elif answer == 4:
    sys.exit()