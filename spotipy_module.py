import spotipy
import spotipy.util as util

class Spotify():
    __s = None # Spotify instance
    __user = None

    def __init__(self, user):
        """
        Init Spotify instance and logon
        """

        self.__user = user

        token = util.prompt_for_user_token(
            user.SPOTIFY_USER_NAME,
            client_id=user.SPOTIFY_CLIENT_ID,
            client_secret=user.SPOTIFY_CLIENT_SECRET,
            redirect_uri=user.SPOTIFY_REDIRECT_URI
        )

        self.__s = spotipy.Spotify(auth=token)

    def getFollowedArtistsOfUser(self):
        """
        Loads all followed artists from a user.
        :return: List of SpotifyArtist objects
        """
        spotify = self.__s
        result = []

        process = True
        lastArtistId = None

        # Do while there are more followed artists
        while process:

            # Get next 20 artists
            spotifyResult = spotify.current_user_followed_artists(50, lastArtistId)
            artists = spotifyResult["artists"]["items"]

            if len(artists) == 0:
                process = False
            else:
                # Iterate over next 20 artists
                for i, artist in enumerate(artists):
                    # Remember last artist
                    lastArtistId = artist["id"]

                    # Create SpotifyArtist
                    spotifyArtist = SpotifyArtist()
                    spotifyArtist.id = lastArtistId

                    # Append to result
                    result.append(spotifyArtist)

        return result


    def getAllNewReleases(self):
        """
        Loads all new releases since the last time
        :return: List of SpotifyRelease objects
        """

        spotify = self.__s
        result = []
        lastUpdate = self.__getLastUpdate()
        spotifyMarket = self.__user.SPOTIFY_MARKET

        # Load artists
        artists = self.getFollowedArtistsOfUser()

        # For every artist the user is following
        for artist in artists:
            # Get albums
            albumResult = spotify.artist_albums(artist.id, album_type="album", country=spotifyMarket)
            albums = self.__processAndFilterAlbums(albumResult, lastUpdate)
            # singles and
            singleResult = spotify.artist_albums(artist.id, album_type="single", country=spotifyMarket)
            singles = self.__processAndFilterAlbums(singleResult, lastUpdate)
            # appears on
            appearsOnResult = spotify.artist_albums(artist.id, album_type="appears_on", country=spotifyMarket)
            appearsOn = self.__processAndFilterAlbums(appearsOnResult, lastUpdate)
            pass


        # Filter
        # Convert
        # Return
        return result

    def __processAndFilterAlbums(self, result, lastUpate):

        pass

    def __getLastUpdate(self):
        pass


class SpotifyRelease():
    """
    Data access object for a Spotify release.
    """
    id = None
    link = None
    artist = None
    title = None
    href = None
    spotifyUri = None
    type = None
    availableMarkets = None
    releaseDate = None

class SpotifyArtist():
    """
    Data access object for a Spotify artist.
    """
    id = None