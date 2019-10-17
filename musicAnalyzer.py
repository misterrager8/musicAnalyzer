import pandas as pd
from song import song
import random

dataframe = pd.read_csv("data.csv")
songList = []

#for index, row in dataframe.iterrows():
#  x = song(row.songName, row.artist, row.album, row.genre, row.yearReleased, row.plays)
#  songList.append(x)
#
#y = random.choice(songList)
#print(y.getAlbum())

avgPlays = dataframe.groupby("albumTitle").mean().sort_values(by = "plays", ascending=True)[:10]
numArtists = dataframe.groupby("artist")["songName"].nunique().sort_values(ascending=False)[:10]

#statsList = open("stats.txt", "w")
#statsList.write(avgPlays.to_string())
#statsList.close

print(avgPlays)
print(numArtists)