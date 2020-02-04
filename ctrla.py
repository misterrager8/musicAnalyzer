from model import *
import MySQLdb

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
        n = album(row[1],
                  row[2],
                  row[3],
                  row[4],
                  str(row[5]),
                  row[6])
        n.toString()
    except MySQLdb.Error, e:
      print(e)
      
    db.close()