from dalang.config.configs import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from dalang.crawling.spotifyconnection import SpotifyConnection
from dalang.crawling.spotifyidcrawler import SpotifyIDCrawler

spotify_connection = SpotifyConnection(
    SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
)
spotify_id_crawler = SpotifyIDCrawler(spotify_connection)
