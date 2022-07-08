from pathlib import Path

from rmn import RMN

from dalang.config.config import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
)
from dalang.crawling.spotifyconnection import SpotifyConnection
from dalang.crawling.spotifyidcrawler import SpotifyIDCrawler
from dalang.crawling.spotifyrecommendationcrawler import (
    SpotifyRecommendationCrawler,
)
from dalang.models.speechbrain import Speechbrain
from dalang.postprocessing.predictionscleaner import (
    PredictionsCleaner,
)
from dalang.tagging.speechbraintocyanitemapper import (
    SpeechbrainToCyaniteMapper,
)


def test_abc():
    spotify_connection = SpotifyConnection(
        SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
    )
    crawler = SpotifyRecommendationCrawler(spotify_connection)
    result = crawler.get_recommendation_by_ids(
        ["2wjbR0QM2uRIz8QacUE494", "5P8KKoAiwhzZkwcBuyhdUi"]
    )
