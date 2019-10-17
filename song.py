class song:
  
  def __init__(self, songName, artist, album, genre, yearReleased, plays):
    self.songName = songName
    self.artist = artist
    self.album = album
    self.genre = genre
    self.yearReleased = yearReleased
    self.plays = plays
    
  def getSongName(self):
    return self.songName
  
  def setSongName(self, x):
    self.songName = x
    
  def getArtist(self):
    return self.artist
  
  def setArtist(self, x):
    self.artist = x
    
  def getAlbum(self):
    return self.album
  
  def setAlbum(self, x):
    self.album = x
    
  def getGenre(self):
    return self.genre
  
  def setGenre(self, x):
    self.genre = x
    
  def getYearReleased(self):
    return self.yearReleased
  
  def setYearReleased(self, x):
    self.yearReleased = x
    
  def getPlays(self):
    return self.plays
  
  def setPlays(self, x):
    self.plays = x