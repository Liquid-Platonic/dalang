from dalang.crawling.spotifyconnection import SpotifyConnection
from dalang.utils.singleton import Singleton


class SpotifyCrawler(metaclass=Singleton):
    def __init__(self, spotify_connection: SpotifyConnection) -> None:
        self.spotify_connection = spotify_connection
