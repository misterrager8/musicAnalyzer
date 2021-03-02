from modules.model import Album, Song


def test_add_songs():
    b = Album("Song Machine Vol. 1")
    b.add_songs([
        Song("Strange Timez"),
        Song("Aries"),
        Song("Pac Man"),
        Song("Pink Phantom")
    ])
    assert b.songs[2].name == "Pac Man"
