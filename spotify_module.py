import spotipy
import spotipy.util as util
from util import getLastUpdate, DATE_FORMAT, saveLastUpdate
from datetime import datetime
from util import log

class SpotifyRelease():
    """
    Data access object for a Spotify release.
    """
    id = None
    link = None
    artist = None
    artists = None
    title = None
    type = None
    releaseDate = None

    def __init__(self, id=None, artists=None, type=None, releaseDate=None, title=None, link=None):
        self.id = id
        self.link = link
        self.title = title
        self.type = type
        self.releaseDate = releaseDate
        self.artists = artists
        self.artist = artists[0]["name"]

    def toTwitterString(self):
        artist = self.artist
        title = self.title
        link = self.link

        restLen = 130 - len(link) - len(artist)
        title = title[:restLen]

        return "%s - %s %s" % (artist, title, link)


class SpotifyArtist():
    """
    Data access object for a Spotify artist.
    """
    id = None
    name = None


class Spotify():
    __s = None  # Spotify instance
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


    def getFullAlbum(self, albumId):
        """
        Returns the full album information for a given album id
        :param albumId: Id from the album you want to look up
        :return: Album as a SpotifyRelease object
        """
        spotify = self.__s
        album = spotify.album(album_id=albumId)
        result = SpotifyRelease(
                id=album["id"],
                artists=album["artists"],
                type=album["type"],
                releaseDate=album["release_date"],
                title=album["name"],
                link=album["external_urls"]["spotify"]
            )
        return result


    def getNLatestAlbumsForArtistOnMarketByType(self, artistId, market="DE", type=type, limit=10):
        """
        Gets you the latest n albums for an artist depending on album type (album, single, appears on) and the market you are looking for
        :param artistId: Id of the artist you want to look up
        :param market: Market you are watching
        :param type: Album type
        :param limit: Limit of Albums between 0 and 20
        :return: List of all albums of a specific type from an artist
        """
        spotify = self.__s

        result = []

        albumResult = spotify.artist_albums(artistId, limit=limit, album_type=type, country=market)
        albums = albumResult["items"]

        # If next set of albums is empty then stop the album loop
        if len(albums) == 0:
            process = False
        else:
            # Iterate over next album set and append the found albums
            for album in albums:
                resultAlbum = self.getFullAlbum(album["id"])
                result.append(resultAlbum)

        return result


    def getAllAlbumsForArtistOnMarketByType(self, artistId, spotifyMarket, type):
        """
        Gets you all albums for an artist depending on album type (album, single, appears on) and the market you are looking for
        :param artistId: Id of the artist you want to look up
        :param spotifyMarket: Market you are watching
        :param type: Album type
        :return: List of all albums of a specific type from an artist
        """
        spotify = self.__s

        result = []
        process = True
        offset = 0

        # loop
        while process:
            albumResult = spotify.artist_albums(artistId, album_type=type, country=spotifyMarket, offset=offset)
            albums = albumResult["items"]

            offset += len(albums)

            # If next set of albums is empty then stop the album loop
            if len(albums) == 0:
                process = False
            else:
                # Iterate over next album set and append the found albums
                for album in albums:
                    resultAlbum = self.getFullAlbum(album["id"])
                    result.append(resultAlbum)
        # end loop

        return result


    def getAlbums(self, artist, spotifyMarket, withAppearsOn=False):
        """
        Gets you all albums from an artist on a Spotify market
        :param artist: SpotifyArtist object of the artist you want to have the albums from
        :param spotifyMarket: The Spotify market which the resulting albums should be available in
        :param withAppearsOn: Decide if you want to receive the appearances too
        :return: List of all albums, singles and sometimes appearances of an artist in a market
        """

        limit = self.__user.NUMBER_OF_RELEASES_TO_LOOK_IN

        # LOGGING
        log("Get albums from %s" % (artist.name))

        albumResult = self.getNLatestAlbumsForArtistOnMarketByType(artist.id, market=spotifyMarket, type="album", limit=limit)
        result = albumResult

        singleResult = self.getNLatestAlbumsForArtistOnMarketByType(artist.id, market=spotifyMarket, type="single", limit=limit)
        result = result + singleResult

        if withAppearsOn:
            appearsOnResult = self.getNLatestAlbumsForArtistOnMarketByType(artist.id, market=spotifyMarket, type="appears_on", limit=limit)
            result = result + appearsOnResult

        return result


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

            # Get next n artists
            artistResult = spotify.current_user_followed_artists(50, lastArtistId)
            artists = artistResult["artists"]["items"]

            if len(artists) == 0:
                process = False
            else:
                # Iterate over next 20 artists
                for i, artist in enumerate(artists):
                    # Remember last artist
                    lastArtistId = artist["id"]

                    # Create SpotifyArtist
                    spotifyArtist = SpotifyArtist()
                    spotifyArtist.id = artist["id"]
                    spotifyArtist.name = artist["name"]

                    # Append to result
                    result.append(spotifyArtist)

        # LOGGING
        log("%s artist found" % (len(result)))

        return result


    def __albumAfterLastUpdateFilter(self, spotifyRelease):
        """
        A filter method for filtering Spotify releases out, that are not younger than the last update date.
        :param spotifyRelease: Object to check.
        :return: Boolean stating if object is younger than the last update date.
        """
        format = DATE_FORMAT

        lastUpdateString = getLastUpdate()
        lastUpdateDate = datetime.strptime(lastUpdateString, format)

        releaseDateString = spotifyRelease.releaseDate
        try:
            # If release date is in YYYY-mm-dd format
            releaseDate = datetime.strptime(releaseDateString, format)
        except ValueError:
            # If release date is in YYYY format
            releaseDate = datetime.strptime("%s-01-01" % (releaseDateString), format)

        return releaseDate >= lastUpdateDate

    def getAllNewReleases(self):
        """
        Loads all new releases since the last time
        :return: List of SpotifyRelease objects
        """

        result = []
        spotifyMarket = self.__user.SPOTIFY_MARKET

        # Load artists
        artists = self.getFollowedArtistsOfUser()

        # For every artist the user is following
        for artist in artists:
            # Get the albums
            albums = self.getAlbums(artist, spotifyMarket)
            # Filter them
            filteredAlbums = list(filter(self.__albumAfterLastUpdateFilter, albums))
            # and append to the result
            result = result + filteredAlbums

        return result