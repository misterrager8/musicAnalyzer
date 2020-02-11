import csv
from ctrla import *
from model import *

albumCtrla = ctrla()
r = albumCtrla.viewAlbums()
results = []

for submission in r:
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

del results[:]