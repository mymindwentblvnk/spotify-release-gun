from spotipy_module import *
from config import *

user = User()
s = Spotify(user)
#list = s.getAlbums("0b2XeWDPeBiLeskT6RFqMb", "DE")
result = s.getAllNewReleases()
#print(len(s.getFollowedArtistsOfUser()))
print(len(result))

