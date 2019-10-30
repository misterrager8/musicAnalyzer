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
  resultBox.delete(0, Tkinter.END)
  avgPlays = dataframe.groupby("albumTitle")["plays"].mean().sort_values(ascending=False)[:num]
  for key, value in avgPlays.iteritems():
    resultBox.insert(Tkinter.END, key)
  
def getTopArtists(num):
  resultBox.delete(0, Tkinter.END)
  numArtists = dataframe.groupby("artist")["plays"].sum().sort_values(ascending=False)[:num]
  for key, value in numArtists.iteritems():
    resultBox.insert(Tkinter.END, key)
  
def exportTXT():
  avgPlays2 = dataframe.groupby("albumTitle")["plays"].mean().sort_values(ascending=False)
  avgPlays2.to_csv("albums.csv", header=False)
#  statsList = open("albums.txt", "w")
#  statsList.write(avgPlays2.encode("utf-8"))
#  statsList.close
  
def getAlbumByYear(year):
  resultBox.delete(0, Tkinter.END)
  results = []
  for i in songList:
    if i.album not in results and i.yearReleased == year:
      results.append(i.album)
  for i in results:
    resultBox.insert(Tkinter.END, i)
    
def getTopSongs(num):
  resultBox.delete(0, Tkinter.END)
  sortedList = sorted(songList, key = lambda x: x.plays, reverse = True)
  for i in range(0, num):
    resultBox.insert(Tkinter.END, sortedList[i].songName)
      
mainWindow = Tkinter.Tk()
mainWindow.title("Music DB")

numField = Tkinter.Entry(mainWindow)
numField.pack()

submitButton = Tkinter.Button(mainWindow, text = "Random Albums", command = lambda: getRandomAlbums(int(numField.get())))
submitButton.pack()

submitButton2 = Tkinter.Button(mainWindow, text = "Top Albums", command = lambda: getTopAlbums(int(numField.get())))
submitButton2.pack()

submitButton3 = Tkinter.Button(mainWindow, text = "Top Artists", command = lambda: getTopArtists(int(numField.get())))
submitButton3.pack()

submitButton4 = Tkinter.Button(mainWindow, text = "Albums By Year", command = lambda: getAlbumByYear(int(numField.get())))
submitButton4.pack()

submitButton5 = Tkinter.Button(mainWindow, text = "Top Songs", command = lambda: getTopSongs(int(numField.get())))
submitButton5.pack()

submitButton6 = Tkinter.Button(mainWindow, text = "Export Ranked Albums", command = exportTXT)
submitButton6.pack()

resultBox = Tkinter.Listbox(mainWindow)
resultBox.pack()

mainWindow.mainloop()