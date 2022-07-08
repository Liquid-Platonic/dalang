from dalang.config.configs import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from dalang.crawling.spotifyconnection import SpotifyConnection
from dalang.crawling.spotifyidcrawler import SpotifyIDCrawler
from dalang.crawling.spotifyrecommendationscrawler import (
    SpotifyRecommendationsCrawler,
)
from dalang.tagging.distilberttokeywordsmapper import DistilbertToCyaniteMapper
from dalang.tagging.speechbraintokeywordsmapper import (
    SpeechbrainToCyaniteMapper,
)


def test_crawler():
    mapper = DistilbertToCyaniteMapper()
    result = mapper.map(
        {
            "sadness": 0.5,
            "joy": 0.5,
            "love": 0.5,
            "anger": 0.5,
            "fear": 0.5,
            "surprise": 0.5,
        }
    )
    x = 5
