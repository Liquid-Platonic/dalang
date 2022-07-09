from dalang.config.configs import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from dalang.crawling.spotifyconnection import SpotifyConnection
from dalang.crawling.spotifyidcrawler import SpotifyIDCrawler
from dalang.crawling.spotifyrecommendationscrawler import (
    SpotifyRecommendationsCrawler,
)

spotify_connection = SpotifyConnection(
    SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
)
spotify_id_crawler = SpotifyIDCrawler(spotify_connection)
spotify_recommendations_crawler = SpotifyRecommendationsCrawler(
    spotify_connection
)
