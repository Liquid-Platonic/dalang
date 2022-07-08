from typing import List, Tuple

from dalang.apis.cyaniteapi import CyaniteApi
from dalang.tagging import TagPredictions
from dalang.tagging.cyanitegenretokeywordsmapper import (
    CyaniteGenreToKeywordsMapper,
)


class Cyanite:
    def __init__(
        self,
        cyanite_api: CyaniteApi = CyaniteApi(),
        cyanite_genre_mapper: CyaniteGenreToKeywordsMapper = CyaniteGenreToKeywordsMapper(),
    ) -> None:
        self.cyanite_api = cyanite_api
        self.cyanite_genre_mapper = cyanite_genre_mapper

    def predict(self, spotify_ids: List[str]) -> List[Tuple[TagPredictions]]:
        results = {"genres": [], "moods": []}
        for spotify_id in spotify_ids:
            genre, mood = self.cyanite_api.get_moods_and_genres(spotify_id)
            results["genres"].append(self.cyanite_genre_mapper.map(genre))
            results["moods"].append(mood)
        return results
