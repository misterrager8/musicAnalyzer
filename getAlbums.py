import csv
from ctrla import *
from model import *
import sys

albumCtrla = ctrla()

def allAlbums():
  results = []
  for submission in albumCtrla.viewAlbums():
    results.append([submission.albumID,
                   submission.title,
                   submission.artist,
                   submission.genre,
                   submission.releaseDate,
                   submission.rating,
                   submission.tags])

  with open("albumsList.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(results)

def searchedAlbums(term, searchType):
  results = []
  for submission in albumCtrla.searchAlbums(term, searchType):
    results.append([submission.albumID,
                   submission.title,
                   submission.artist,
                   submission.genre,
                   submission.releaseDate,
                   submission.rating,
                   submission.tags])

  with open("albumsList.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(results)
    
if __name__ == "__main__":
  if len(sys.argv) < 2:
    allAlbums()
  else:
    searchedAlbums(sys.argv[1], sys.argv[2])