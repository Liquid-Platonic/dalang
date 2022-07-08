from typing import List

from dalang.crawling.spotifycrawler import SpotifyCrawler
from dalang.utils.singleton import Singleton


class SpotifyRecommendationsCrawler(SpotifyCrawler, metaclass=Singleton):
    def get_recommendation_by_ids(
        self, spotify_ids: List[str], num_recoms: int = 10
    ) -> list:
        recommendations = self.spotify_connection().recommendations(
            seed_tracks=spotify_ids, limit=num_recoms
        )
        return [
            (track["id"], track["artists"][0]["name"], track["name"])
            for track in recommendations["tracks"]
        ]
