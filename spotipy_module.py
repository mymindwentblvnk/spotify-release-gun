import spotipy
import spotipy.util as util
from util import getLastUpdate, DATE_FORMAT, saveLastUpdate
import time


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

                    # LOGGING
                    print("Artist %s found" % (artist["name"]))

                    # Create SpotifyArtist
                    spotifyArtist = SpotifyArtist()
                    spotifyArtist.id = artist["id"]
                    spotifyArtist.name = artist["name"]

                    # Append to result
                    result.append(spotifyArtist)

        return result

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
            albums = self.getAlbums(artist, spotifyMarket)

            filteredAlbums = list(filter(self.__albumAfterLastUpdateFilter, albums))

            result = result + filteredAlbums

        # Save this date as last update date
        saveLastUpdate()

        return result


    def __albumAfterLastUpdateFilter(self, spotifyRelease):
        """
        A filter method for filtering Spotify releases out, that are not younger than the last update date.
        :param spotifyRelease: Object to check.
        :return: Boolean stating if object is younger than the last update date.
        """
        format = DATE_FORMAT

        lastUpdate = getLastUpdate()
        releaseDate = spotifyRelease.releaseDate

        lastUpdateDate = time.strptime(lastUpdate, format)
        try:
            # If release date is in YYYY-mm-dd format
            releaseDateDate = time.strptime(releaseDate, format)
        except ValueError:
            # If release date is in YYYY format
            releaseDateDate = time.strptime("%s-01-01" % (releaseDate), format)

        return releaseDateDate >= lastUpdateDate


    def getAlbums(self, artist, spotifyMarket, withAppearsOn=False):
        """
        Gets you all albums from an artist on a Spotify market
        :param artist: SpotifyArtist object of the artist you want to have the albums from
        :param spotifyMarket: The Spotify market which the resulting albums should be available in
        :param withAppearsOn: Decide if you want to receive the appearances too
        :return: List of all albums, singles and sometimes appearances of an artist in a market
        """

        # LOGGING
        print("Get albums from %s" % (artist.name))

        albumResult = self.getNLatestAlbumsForArtistOnMarketByType(artist.id, market=spotifyMarket, type="album")
        result = albumResult

        singleResult = self.getNLatestAlbumsForArtistOnMarketByType(artist.id, market=spotifyMarket, type="single")
        result = result + singleResult


        if withAppearsOn:
            appearsOnResult = self.getNLatestAlbumsForArtistOnMarketByType(artist.id, market=spotifyMarket, type="appears_on")
            result = result + appearsOnResult

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

    def getFullAlbum(self, albumId):
        """
        Returns the full album information for a given album id
        :param albumId: Id from the album you want to look up
        :return: Album as a SpotifyRelease object
        """
        spotify = self.__s
        album = spotify.album(album_id=albumId)
        result = SpotifyRelease()
        result.id = album["id"]
        result.artist = album["artists"][0]["name"] #TODO All artists
        result.type = album["type"]
        result.releaseDate = album["release_date"]
        result.title = album["name"]
        result.link = album["external_urls"]["spotify"]
        return result


class SpotifyRelease():
    """
    Data access object for a Spotify release.
    """
    id = None
    link = None
    artist = None
    title = None
    href = None
    url = None
    type = None
    availableMarkets = None
    releaseDate = None

    def toTwitterString(self):
        artistString = self.artist
        titleString = self.title
        linkString = self.link

        restLen = 130 - len(linkString) - len(artistString)
        titleString = titleString[:restLen]

        return "%s - %s %s" % (artistString, titleString, linkString)


class SpotifyArtist():
    """
    Data access object for a Spotify artist.
    """
    id = None
    name = None
