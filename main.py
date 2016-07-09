from spotipy_module import *
from config import *

user = User()
s = Spotify(user)

result = s.getAllNewReleases()