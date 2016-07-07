from spotipy_module import *
from config import getUser

user = getUser()
s = Spotify(user)
#result = s.getAllNewReleases()
print(len(s.getFollowedArtistsOfUser()))