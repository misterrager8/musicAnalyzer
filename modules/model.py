class Album:
    """
    Class for Album object.

    Attributes:
    albumID -- Unique identifier for Album
    title -- Album title
    artist -- Album artist
    genre -- Genre the Album belongs to
    release_date -- Release date for the Album. Can be year or specific date
    rating -- Numerical rating of Album from 0.0 to 5.0
    tags -- User-defined identifiers for Album to make searching, organizing easier
    """

    def __init__(self, album_id, title, artist, genre, release_date, rating, tags, genius_url):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.genre = genre
        self.release_date = release_date
        self.rating = rating
        self.tags = tags
        self.genius_url = genius_url

    def get_title(self):
        return self.title

    def get_artist(self):
        return self.artist

    def get_genre(self):
        return self.genre

    def get_release_date(self):
        return self.release_date

    def get_rating(self):
        return self.rating

    def get_tags(self):
        return self.tags

    def get_genius_url(self):
        return self.genius_url

    def set_title(self, title):
        self.title = title

    def set_artist(self, artist):
        self.artist = artist

    def set_genre(self, genre):
        self.genre = genre

    def set_release_date(self, release_date):
        self.release_date = release_date

    def set_rating(self, rating):
        self.rating = rating

    def set_tags(self, tags):
        self.tags = tags

    def set_genius_url(self, genius_url):
        self.genius_url = genius_url

    def to_string(self):
        print(self.album_id,
              str(self.title),
              str(self.artist),
              str(self.genre),
              str(self.release_date),
              str(self.rating),
              str(self.tags),
              str(self.genius_url))
