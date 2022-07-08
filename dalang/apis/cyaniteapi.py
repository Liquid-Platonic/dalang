from ast import keyword
from typing import List, Tuple

import requests

from dalang.config.configs import ACCESS_TOKEN, API_URL
from dalang.tagging import TagPredictions
from dalang.tagging.cyanitegenretokeywordsmapper import (
    CyaniteGenreToKeywordsMapper,
)
from dalang.tagging.tags import CyaniteGenres, CyaniteMoods


class CyaniteApi:
    def __init__(self, access_token: str = ACCESS_TOKEN, api_url: str = API_URL) -> None:
        self.headers = {"Authorization": f"Bearer {access_token}"}
        self.api_url = api_url

    @property
    def genres(self) -> List[str]:
        return "\n".join(CyaniteGenres.to_list())

    @property
    def moods(self) -> List[str]:
        return "\n".join(CyaniteMoods.to_list())

    def _query_and_get_results(self, query):
        r = requests.post(self.api_url, json={"query": query}, headers=self.headers)
        if r.status_code == 200:
            return r.json()
        else:
            raise Exception(f"Query failed to run with a {r.status_code}.")

    def get_moods_and_genres(self, spotify_id: str) -> Tuple[TagPredictions]:
        query = f"""
        {{
            spotifyTrack(id: "{spotify_id}") {{
                ... on SpotifyTrack {{
                    audioAnalysisV6 {{
                        ... on AudioAnalysisV6Finished {{
                            result {{
                                genre {{
                                    {self.genres}
                                }}
                                mood {{
                                    {self.moods}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }}
        """
        results = self._query_and_get_results(query)["data"]["spotifyTrack"]["audioAnalysisV6"][
            "result"
        ]
        return results["genre"], results["mood"]

    @staticmethod
    def _convert_keywords_to_str(keywords: TagPredictions) -> str:
        #  keyword: "sad", weight: 1
        keywords_str = "["
        for name, weight in keywords.items():
            keywords_str += f'{{keyword: "{name}", weight: {weight}}}'
        keywords_str += "]"
        return keywords_str

    def get_spotify_ids_by_keywords(self, keywords: TagPredictions) -> List[str]:
        query = f"""
            query KeywordSearchQuery {{
                keywordSearch(
                    target: {{ spotify: {{}} }}
                    keywords: {self._convert_keywords_to_str(keywords)}
                ) {{
                    __typename
                    ... on KeywordSearchError {{
                        message
                        code
                    }}
                    ... on KeywordSearchConnection {{
                        edges {{
                            node {{
                                ... on SpotifyTrack {{
                                    id
                                }}
                            }}
                        }}
                    }}
                }}
            }}
            """
        edges = self._query_and_get_results(query)["data"]["keywordSearch"]["edges"]
        return [edge["node"]["id"] for edge in edges]
