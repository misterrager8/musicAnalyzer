from model import *
import MySQLdb
import csv

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
    db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
    cursor = db.cursor()
    sql = "SELECT * FROM albums"
    
    try:
      cursor.execute(sql)
      results = cursor.fetchall()
      for row in results:
        print(row[0],
              row[1],
              row[2],
              row[3],
              row[4],
              str(row[5]),
              row[6])
        
    except MySQLdb.Error, e:
      print(e)
      
    db.close()
    
  def searchAlbums(self, c):
    db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
    cursor = db.cursor()
    sql = "SELECT * FROM albums WHERE title LIKE %s", ("%{}%".format(c),)
    
    try:
      cursor.execute(sql)
      results = cursor.fetchall()
      for row in results:
        print(row[0],
              row[1],
              row[2],
              row[3],
              row[4],
              str(row[5]),
              row[6])
        
    except MySQLdb.Error, e:
      print(e)
      
    db.close()
    
  def exportAlbums(self):
    db = MySQLdb.connect("localhost","root","bre9ase4","TESTDB")
    cursor = db.cursor()
    sql = "SELECT * FROM albums"
    
    try:
      cursor.execute(sql)
      results = cursor.fetchall()
      
      with open("albums.csv", "w") as f:
          a = csv.writer(f, delimiter = ",")
          a.writerow(["Album ID", "Title", "Artist", "Genre", "Release Date", "Rating", "Tags"])
          a.writerows(results)
        
    except MySQLdb.Error, e:
      print(e)
      
    db.close()
    print("Exported.")