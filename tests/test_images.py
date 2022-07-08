from dalang.config.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from dalang.crawling.spotifyconnection import SpotifyConnection
from dalang.crawling.spotifyidcrawler import SpotifyIDCrawler
from dalang.crawling.spotifyrecommendationscrawler import (
    SpotifyRecommendationsCrawler,
)


def test_crawler():
    spotify_connection = SpotifyConnection(
        SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
    )
    crawler = SpotifyIDCrawler(spotify_connection)
    result = crawler.get_id_by_title("squarepusher - red hot car")
    crawler = SpotifyRecommendationsCrawler(spotify_connection)
    result = crawler.get_recommendation_by_ids([result])
    x = 5
