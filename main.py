import modules.ctrla
from modules.model import Album

if __name__ == "__main__":
    m = Album("test album", 4, "fff")
    modules.ctrla.DB().create(m)
