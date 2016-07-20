import spotipy
import spotipy.util as util
from file_operations import get_last_update, DATE_FORMAT, save_last_update
from datetime import datetime
from the_logger import log


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
    release_date = None

    def __init__(self, id=None, artists=None, type=None, release_date=None,
                 title=None, link=None):
        self.id = id
        self.link = link
        self.title = title
        self.type = type
        self.release_date = release_date
        self.artists = artists
        self.artist = artists[0]["name"]

    def to_twitter_string(self):
        artist = self.artist
        title = self.title
        link = self.link

        rest_len = 130 - len(link) - len(artist)
        title = title[:rest_len]

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


    def get_full_album(self, albumId):
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
                release_date=album["release_date"],
                title=album["name"],
                link=album["external_urls"]["spotify"]
            )
        return result

    def get_n_latest_albums_for_artist_by_type(self, artistId,
                                               market="DE",
                                               type=type,
                                               limit=10):
        """
        Gets you the latest n albums for an artist depending on album type
        (album, single, appears on) and the market you are looking for
        :param artistId: Id of the artist you want to look up
        :param market: Market you are watching
        :param type: Album type
        :param limit: Limit of Albums between 0 and 20
        :return: List of all albums of a specific type from an artist
        """
        spotify = self.__s

        result = []

        albumResult = spotify.artist_albums(artistId, limit=limit,
                                            album_type=type, country=market)
        albums = albumResult["items"]

        # If next set of albums is empty then stop the album loop
        if len(albums) == 0:
            process = False
        else:
            # Iterate over next album set and append the found albums
            for album in albums:
                resultAlbum = self.get_full_album(album["id"])
                result.append(resultAlbum)

        return result

    def get_albums(self, artist, spotify_market, with_appears_on=False):
        """
        Gets you all albums from an artist on a Spotify market
        :param artist: SpotifyArtist object of the artist you want to have the
                albums from
        :param spotify_market: The Spotify market which the resulting albums
                should be available in
        :param with_appears_on: Decide if you want to receive the appearances too
        :return: List of all albums, singles and sometimes appearances of an
                artist in a market
        """

        limit = self.__user.NUMBER_OF_RELEASES_TO_LOOK_IN

        # LOGGING
        log("Get albums from %s" % (artist.name))

        albumResult = self.get_n_latest_albums_for_artist_by_type(
                artist.id, market=spotify_market, type="album", limit=limit)
        result = albumResult

        singleResult = self.get_n_latest_albums_for_artist_by_type(
                artist.id, market=spotify_market, type="single", limit=limit)
        result = result + singleResult

        if with_appears_on:
            appearsOnResult = self.get_n_latest_albums_for_artist_by_type(
                    artist.id, market=spotify_market,
                    type="appears_on", limit=limit)
            result = result + appearsOnResult

        return result

    def get_followed_artists_of_user(self):
        """
        Loads all followed artists from a user.
        :return: List of SpotifyArtist objects
        """
        spotify = self.__s
        result = []

        process = True
        last_artist_id = None

        # Do while there are more followed artists
        while process:

            # Get next n artists
            artistResult = spotify.current_user_followed_artists(
                    50, last_artist_id)
            artists = artistResult["artists"]["items"]

            if len(artists) == 0:
                process = False
            else:
                # Iterate over next 20 artists
                for i, artist in enumerate(artists):
                    # Remember last artist
                    last_artist_id = artist["id"]

                    # Create SpotifyArtist
                    spotifyArtist = SpotifyArtist()
                    spotifyArtist.id = artist["id"]
                    spotifyArtist.name = artist["name"]

                    # Append to result
                    result.append(spotifyArtist)

        # LOGGING
        log("%s artist found" % (len(result)))

        return result

    def get_all_new_releases(self):
        """
        Loads all new releases since the last time
        :return: List of SpotifyRelease objects
        """

        def album_after_last_update_filter(spotifyRelease):
            """
            A filter method for filtering Spotify releases out, that are not
            younger than the last update date.
            :param spotifyRelease: Object to check.
            :return: Boolean stating if object is younger than the last
                    update date.
            """
            format = DATE_FORMAT

            last_update_string = get_last_update()
            last_update_date = datetime.strptime(last_update_string, format)

            release_date_string = spotifyRelease.release_date
            try:
                # If release date is in YYYY-mm-dd format
                release_date = datetime.strptime(release_date_string, format)
            except ValueError:
                # If release date is in YYYY format
                release_date = datetime.strptime(
                    "%s-01-01" % (release_date_string), format)

            return release_date >= last_update_date

        result = []
        spotify_market = self.__user.SPOTIFY_MARKET

        # Load artists
        artists = self.get_followed_artists_of_user()

        # For every artist the user is following
        for artist in artists:
            # Get the albums
            albums = self.get_albums(artist, spotify_market)
            # Filter them
            filtered_albums = list(
                filter(album_after_last_update_filter, albums)
            )
            # and append to the result
            result = result + filtered_albums

        return result
