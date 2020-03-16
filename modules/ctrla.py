from model import *
import MySQLdb
import csv
import sys
import os

class ctrla():
  def __init__(self):
    pass
  
  def runQuery(self, query):
    """Executes general SQL command"""
    db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
    cursor = db.cursor()
    
    try:
      cursor.execute(query)
      db.commit()
    except MySQLdb.Error, e:
      print(e)
      
    db.close()
  
  def runReadQuery(self, query):
    """Executes SQL SELECT command"""
    db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
    cursor = db.cursor()
    
    try:
      cursor.execute(query)
      return cursor.fetchall()
    except MySQLdb.Error, e:
      print(e)
  
  def runSearchQuery(self, query, term):
    """Executes SQL WHERE/LIKE command"""
    db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
    cursor = db.cursor()
    
    try:
      cursor.execute(query, ("%" + term + "%",))
      return cursor.fetchall()
    except MySQLdb.Error, e:
      print(e)
  
  def addAlbum(self, newAlbum):
    """Adds album to DB"""
    sql = "INSERT INTO albums (title, artist, genre, releaseDate, rating, tags) VALUES ('%s', '%s', '%s', '%s', '%d', '%s')" % (newAlbum.title, newAlbum.artist, newAlbum.genre, newAlbum.releaseDate, newAlbum.rating, newAlbum.tags)
    self.runQuery(sql)
  
  def deleteAlbum(self, albumID):
    """Deletes album from DB"""
    sql = "DELETE FROM albums WHERE albumID = '%d'" % (albumID)
    self.runQuery(sql)
  
  def editAlbum(self, albumID, searchType, change):
    """Edits info of selected album according to user's choice"""
    sql0 = "UPDATE albums SET title = '%s' WHERE albumID = '%d'" % (change, albumID)
    sql1 = "UPDATE albums SET artist = '%s' WHERE albumID = '%d'" % (change, albumID)
    sql2 = "UPDATE albums SET releaseDate = '%s' WHERE albumID = '%d'" % (change, albumID)
    sql3 = "UPDATE albums SET rating = '%s' WHERE albumID = '%d'" % (change, albumID)
    sql4 = "UPDATE albums SET tags = '%s' WHERE albumID = '%d'" % (change, albumID)
    
    if searchType == 0:
      self.runQuery(sql0)
    elif searchType == 1:
      self.runQuery(sql1)
    elif searchType == 2:
      self.runQuery(sql2)
    elif searchType == 3:
      self.runQuery(sql3)
    elif searchType == 4:
      self.runQuery(sql4)

    print("Album edited.")
  
  def deleteAllAlbums(self):
    """Deletes all albums in the DB, and also resets albumID's to 0"""
    sql = "TRUNCATE TABLE albums"
    self.runQuery(sql)
    
  def viewAlbums(self):
    """Gets all albums in DB, and stores them in a list"""
    albumsList = []
    sql = "SELECT * FROM albums"
    
    for row in self.runReadQuery(sql):
      x = album(row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6])
      albumsList.append(x)
      
    return albumsList
    
  def searchAlbums(self, term, searchType):
    """Search albums by specified column"""
    albumsList = []
    b = {}
    sql0 = "SELECT * FROM albums WHERE title LIKE %s"
    sql1 = "SELECT * FROM albums WHERE artist LIKE %s"
    sql2 = "SELECT * FROM albums WHERE tags LIKE %s"
    sql3 = "SELECT * FROM albums WHERE releaseDate LIKE %s"
    
    if int(searchType) == 0:
      b = self.runSearchQuery(sql0, term)
    elif int(searchType) == 1:
      b = self.runSearchQuery(sql1, term)
    elif int(searchType) == 2:
      b = self.runSearchQuery(sql2, term)
    elif int(searchType) == 3:
      b = self.runSearchQuery(sql3, term)
      
    for row in b:
      x = album(row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6])
      albumsList.append(x)
      
    return albumsList
    
  def exportAlbums(self):
    """Exports all albums to csv file"""
    sql = "SELECT * FROM albums"
    results = self.runReadQuery(sql)

    with open("output.csv", "w") as f:
        a = csv.writer(f, delimiter = ",")
        a.writerow(["Album ID", "Title", "Artist", "Genre", "Release Date", "Rating", "Tags"])
        a.writerows(results)
        
    print("Exported.")
  
  def importAlbums(self):
    """Takes all info from CSV, stores in DB"""
    imported = []
    csv_data = csv.reader(file("input.csv"))
    for row in csv_data:
      qAlbum = album(None, row[0], row[1], row[2], row[3], float(row[4]), row[5])
      imported.append(qAlbum)
      
    for item in imported:
      item.toString()
      
    answer = raw_input("Add these albums? ")
    if answer == "Y" or answer == "y":
      for item in imported:
        self.addAlbum(item)
      
  def GUIviewAlbums(self):
    """Gets all albums in DB, writes to CSV for display on a JTable"""
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
    """Search albums by specified column, writes to CSV for display on a JTable"""
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
    """Deletes album in DB straight from JTable"""
    self.deleteAlbum(albumID)
    self.GUIviewAlbums()
  
  def GUIaddAlbum(self):
    """Adds album to DB from Desktop GUI"""
    csv_data = csv.reader(file("temp.csv"))
    for row in csv_data:
      sql = "INSERT INTO albums (title, artist, genre, releaseDate, rating, tags) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (row[1], row[2], row[3], row[4], row[5], row[6])
      self.runQuery(sql)
    
    os.remove("temp.csv")
    self.GUIviewAlbums()
  
  def GUIeditAlbum(self):
    """Edits info of selected album according to user's choice, straight from JTable"""
    csv_data = csv.reader(file("temp.csv"))
    for row in csv_data:
      sql = "UPDATE albums SET title = '%s', artist = '%s', genre = '%s', releaseDate = '%s', rating = '%s', tags = '%s' WHERE albumID = '%d'" % (row[1], row[2], row[3], row[4], row[5], row[6], int(row[0]))
      self.runQuery(sql)
    
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