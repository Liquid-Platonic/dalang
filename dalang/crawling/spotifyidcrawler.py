from typing import List, Optional

from dalang.crawling.spotifycrawler import SpotifyCrawler


class SpotifyIDCrawler(SpotifyCrawler):
    def get_id_by_title(self, song_title: str) -> Optional[str]:
        result = self._search_query(song_title)
        items = result["tracks"]["items"]
        if not items:
            return None
        return items[0]["id"]

    def get_ids_by_titles(self, song_titles: List[str]) -> List[str]:
        ids = [self.get_id_by_title(title) for title in song_titles]
        return list(filter(None, ids))

    def _search_query(self, query: str) -> List[str]:
        return self.spotify_connection().search(query)
