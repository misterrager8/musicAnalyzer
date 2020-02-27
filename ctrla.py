from model import *
import MySQLdb
import csv
import sys
import os

class ctrla():
  def __init__(self):
    pass
  
  def addAlbum(self, newAlbum):
    db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
    cursor = db.cursor()
    sql = "INSERT INTO albums (title, artist, genre, releaseDate, rating, tags) VALUES ('%s', '%s', '%s', '%s', '%d', '%s')" % (newAlbum.title, newAlbum.artist, newAlbum.genre, newAlbum.releaseDate, newAlbum.rating, newAlbum.tags)
    
    try:
      cursor.execute(sql)
      db.commit()
    except MySQLdb.Error, e:
      print(e)
      
    db.close()
  
  def deleteAlbum(self, albumID):
    db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
    cursor = db.cursor()
    sql = "DELETE FROM albums WHERE albumID = '%d'" % (albumID)
    
    try:
      cursor.execute(sql)
      db.commit()
    except MySQLdb.Error, e:
      print(e)
      
    db.close()
  
  def editAlbum(self, albumID, searchType, change):
    db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
    cursor = db.cursor()
    
    try:
      if searchType == 0:
        cursor.execute("UPDATE albums SET title = '%s' WHERE albumID = '%d'" % (change, albumID))
      elif searchType == 1:
        cursor.execute("UPDATE albums SET artist = '%s' WHERE albumID = '%d'" % (change, albumID))
      elif searchType == 2:
        cursor.execute("UPDATE albums SET releaseDate = '%s' WHERE albumID = '%d'" % (change, albumID))
      elif searchType == 3:
        cursor.execute("UPDATE albums SET rating = '%s' WHERE albumID = '%d'" % (change, albumID))
      elif searchType == 4:
        cursor.execute("UPDATE albums SET tags = '%s' WHERE albumID = '%d'" % (change, albumID))
      db.commit()
    except MySQLdb.Error, e:
      print(e)
     
    db.close()
    print("Album edited.")
  
  def deleteAllAlbums(self):
    db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
    cursor = db.cursor()
    sql = "TRUNCATE TABLE albums"
    
    try:
      cursor.execute(sql)
      db.commit()
    except MySQLdb.Error, e:
      print(e)
      
    db.close()
    
  def viewAlbums(self):
    albumsList = []
    db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
    cursor = db.cursor()
    sql = "SELECT * FROM albums"
    
    try:
      cursor.execute(sql)
      results = cursor.fetchall()
      for row in results:
        x = album(row[0],
              row[1],
              row[2],
              row[3],
              row[4],
              row[5],
              row[6])
        albumsList.append(x)
        
    except MySQLdb.Error, e:
      print(e)
      
    db.close()
    return albumsList
    
  def searchAlbums(self, term, searchType):
    albumsList = []
    db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
    cursor = db.cursor()
    
    try:
      if int(searchType) == 0:
        cursor.execute("SELECT * FROM albums WHERE title LIKE %s", ("%" + term + "%",))
      elif int(searchType) == 1:
        cursor.execute("SELECT * FROM albums WHERE artist LIKE %s", ("%" + term + "%",))
      elif int(searchType) == 2:
        cursor.execute("SELECT * FROM albums WHERE tags LIKE %s", ("%" + term + "%",))
      elif int(searchType) == 3:
        cursor.execute("SELECT * FROM albums WHERE releaseDate LIKE %s", ("%" + term + "%",))
      results = cursor.fetchall()
      for row in results:
        x = album(row[0],
              row[1],
              row[2],
              row[3],
              row[4],
              row[5],
              row[6])
        albumsList.append(x)
        
    except MySQLdb.Error, e:
      print(e)
      
    db.close()
    return albumsList
    
  def exportAlbums(self):
    db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
    cursor = db.cursor()
    sql = "SELECT * FROM albums"
    
    try:
      cursor.execute(sql)
      results = cursor.fetchall()
      
      with open("output.csv", "w") as f:
          a = csv.writer(f, delimiter = ",")
          a.writerow(["Album ID", "Title", "Artist", "Genre", "Release Date", "Rating", "Tags"])
          a.writerows(results)
        
    except MySQLdb.Error, e:
      print(e)
      
    db.close()
    print("Exported.")
  
  def importAlbums(self):
    db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
    cursor = db.cursor()
    
    csv_data = csv.reader(file("input.csv"))
    for row in csv_data:
      cursor.execute("INSERT INTO albums (title, artist, genre, releaseDate, rating, tags) VALUES (%s, %s, %s, %s, %s, %s)", row)
      
    db.commit()  
    db.close()
    
  def GUIviewAlbums(self):
    results = []
    for submission in self.viewAlbums():
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
  
  def GUIsearchAlbums(self, term, searchType):
    results = []
    for submission in self.searchAlbums(term, searchType):
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
  
  def GUIdeleteAlbum(self, albumID):
    self.deleteAlbum(albumID)
    self.GUIviewAlbums()
  
  def GUIaddAlbum(self):
    db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
    cursor = db.cursor()
    
    csv_data = csv.reader(file("temp.csv"))
    for row in csv_data:
      params = [row[1], row[2], row[3], row[4], row[5], row[6]]
      cursor.execute("INSERT INTO albums (title, artist, genre, releaseDate, rating, tags) VALUES (%s, %s, %s, %s, %s, %s)", params)
      
    db.commit()  
    db.close()
    
    os.remove("temp.csv")
    self.GUIviewAlbums()
  
  def GUIeditAlbum(self):
    db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
    cursor = db.cursor()
    
    csv_data = csv.reader(file("temp.csv"))
    for row in csv_data:
      params = [row[1], row[2], row[3], row[4], row[5], row[6], row[0]]
      cursor.execute("UPDATE albums SET title = %s, artist = %s, genre = %s, releaseDate = %s, rating = %s, tags = %s WHERE albumID = %s", params)
      
    db.commit()  
    db.close()
    
    os.remove("temp.csv")
    self.GUIviewAlbums()
    
if __name__ == "__main__":
  albumCtrla = ctrla()
  if len(sys.argv) == 1:
    albumCtrla.GUIviewAlbums()
  elif sys.argv[1] == "search":
    albumCtrla.GUIsearchAlbums(sys.argv[2], int(sys.argv[3]))
  elif sys.argv[1] == "del":
    albumCtrla.GUIdeleteAlbum(int(sys.argv[2]))
  elif sys.argv[1] == "add":
    albumCtrla.GUIaddAlbum()
  elif sys.argv[1] == "edit":
    albumCtrla.GUIeditAlbum()