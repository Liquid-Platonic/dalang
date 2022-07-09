from dalang.config.configs import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from dalang.crawling.spotifyconnection import SpotifyConnection
from dalang.crawling.spotifyidcrawler import SpotifyIDCrawler
from dalang.crawling.spotifyrecommendationscrawler import (
    SpotifyRecommendationsCrawler,
)
from dalang.helpers import merge_dicts


def test_crawler():
    result = merge_dicts(
        [{"angry": 0.5, "happy": 0.6}, {"dance": 0.2, "funk": 0.3}]
    )
    x = 5
