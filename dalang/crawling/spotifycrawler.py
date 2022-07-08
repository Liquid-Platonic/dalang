from dalang.crawling.spotifyconnection import SpotifyConnection


class SpotifyCrawler:
    def __init__(self, spotify_connection: SpotifyConnection):
        self.spotify_connection = spotify_connection
