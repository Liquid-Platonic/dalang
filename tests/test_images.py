from dalang.config.configs import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from dalang.crawling.spotifyconnection import SpotifyConnection
from dalang.crawling.spotifyidcrawler import SpotifyIDCrawler
from dalang.crawling.spotifyrecommendationscrawler import (
    SpotifyRecommendationsCrawler,
)
from dalang.tagging.speechbraintocyanitemapper import (
    SpeechbrainToCyaniteMapper,
)


def test_crawler():
    mapper = SpeechbrainToCyaniteMapper()
    result = mapper.map({"anger": 0.5, "hap": 0.5, "sad": 0.5, "neutral": 0.5})
    x = 5
