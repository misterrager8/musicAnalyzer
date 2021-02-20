class Album:
    def __init__(self,
                 title: str,
                 artist_id: int, # FK
                 genre: str,
                 release_date: str = None,
                 rating: int = None,
                 album_id: int = None):#PK
        self.title = title
        self.artist_id = artist_id
        self.genre = genre
        self.release_date = release_date
        self.rating = rating
        self.album_id = album_id


class Artist:
    def __init__(self,
                 name: str,
                 hometown: str = None,
                 dob: str = None,
                 artist_id: int = None): # PK
        self.name = name
        self.hometown = hometown
        self.dob = dob
        self.artist_id = artist_id


class Song:
    def __init__(self,
                 name: str,
                 artist_id: int = None, # FK
                 album_id: int = None, # FK
                 play_count: int = None,
                 rating: int = None,
                 last_played: str = None,
                 song_id: int = None): # PK
        self.name = name
        self.artist_id = artist_id
        self.album_id = album_id
        self.play_count = play_count
        self.rating = rating
        self.last_played = last_played
        self.song_id = song_id
