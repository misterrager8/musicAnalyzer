class album:
  """
  Class for album object.

  Attributes:
  albumID -- Unique identifier for album
  title -- Album title
  artist -- Album artist
  genre -- Genre the album belongs to
  releaseDate -- Release date for the album. Can be year or specific date
  rating -- Numerical rating of album from 0.0 to 5.0
  tags -- User-defined identifiers for album to make searching, organizing easier
  """
  def __init__(self, albumID, title, artist, genre, releaseDate, rating, tags):
    self.albumID = albumID
    self.title = title
    self.artist = artist
    self.genre = genre
    self.releaseDate = releaseDate
    self.rating = rating
    self.tags = tags
    
  def getTitle(self):
    return self.title
    
  def getArtist(self):
    return self.artist
    
  def getGenre(self):
    return self.genre
    
  def getReleaseDate(self):
    return self.releaseDate
    
  def getRating(self):
    return self.rating
    
  def getTags(self):
    return self.tags
    
  def setTitle(self, title):
    self.title = title
    
  def setArtist(self, artist):
    self.artist = artist
    
  def setGenre(self, genre):
    self.genre = genre
    
  def setReleaseDate(self, releaseDate):
    self.releaseDate = releaseDate
    
  def setRating(self, rating):
    self.rating = rating
    
  def setTags(self, tags):
    self.tags = tags
    
  def toString(self):
    print(self.albumID,
          str(self.title),
          str(self.artist),
          str(self.genre),
          str(self.releaseDate),
          str(self.rating),
          str(self.tags))