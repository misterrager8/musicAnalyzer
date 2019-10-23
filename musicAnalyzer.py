import pandas as pd
from song import song
import random
import Tkinter
import matplotlib.pyplot as plt
import numpy as np

dataframe = pd.read_csv("data.csv")

songList = [song(row["songName"],
                 row["artist"],
                 row["albumTitle"],
                 row["genre"],
                 row["yearReleased"],
                 row["plays"])
            for index, row in dataframe.iterrows()]

def getRandomAlbums(num):
  resultBox.delete(0, Tkinter.END)
  for i in range(1, num + 1):
    y = random.choice(songList)
    resultBox.insert(Tkinter.END, y.album)
  
def getTopAlbums(num):
  avgPlays = dataframe.groupby("albumTitle")
  abc = avgPlays["plays"].agg(np.mean).nlargest(num)
  abc.plot.barh(y = "albumTitle")
  plt.show()
  
def getTopArtistsByCount(num):
  resultBox.delete(0, Tkinter.END)
  numArtists = dataframe.groupby("artist")["songName"].nunique().sort_values(ascending=False)[:num]
  print(numArtists)
  
def exportTXT():
  statsList = open("stats.txt", "w")
  statsList.write(avgPlays.to_string())
  statsList.close
  
def getAlbumByYear(year):
  resultBox.delete(0, Tkinter.END)
  results = []
  for i in songList:
    if i.album not in results and i.yearReleased == year:
      results.append(i.album)
  for i in results:
    print(i)
    
def getTopSongs():
  resultBox.delete(0, Tkinter.END)
  sortedList = sorted(songList, key = lambda x: x.plays, reverse = True)
  for i in range(0, 24):
    print(sortedList[i].songName + "\t" + str(sortedList[i].plays))
      
mainWindow = Tkinter.Tk()
mainWindow.title("Music DB")

numField = Tkinter.Entry(mainWindow)
numField.pack()

submitButton = Tkinter.Button(mainWindow, text = "Get Random Albums", command = lambda: getRandomAlbums(int(numField.get())))
submitButton.pack()

submitButton2 = Tkinter.Button(mainWindow, text = "Get Top Albums", command = lambda: getTopAlbums(int(numField.get())))
submitButton2.pack()

submitButton3 = Tkinter.Button(mainWindow, text = "Get Top Artists", command = lambda: getTopArtistsByCount(int(numField.get())))
submitButton3.pack()

submitButton4 = Tkinter.Button(mainWindow, text = "Get Albums By Year", command = lambda: getAlbumByYear(int(numField.get())))
submitButton4.pack()

submitButton5 = Tkinter.Button(mainWindow, text = "Get Top Songs", command = getTopSongs)
submitButton5.pack()

resultBox = Tkinter.Listbox(mainWindow)
resultBox.pack()

mainWindow.mainloop()