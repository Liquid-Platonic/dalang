import json

from dalang.apis.utils import query_and_get_results
from dalang.config.configs import ACCESS_TOKEN, API_URL
from dalang.tagging.tags import CyaniteGenres, CyaniteMoods

endpoint = API_URL
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

spotify_id = "7iQM9DQUFKUSNjVt8GQZV2"

## Get genres & moods ###

# genres = "\n".join(CyaniteGenres.to_list())
# moods = "\n".join(CyaniteMoods.to_list())
# query = f"""
# {{
#     spotifyTrack(id: "{spotify_id}") {{
#         ... on SpotifyTrack {{
#             audioAnalysisV6 {{
#                 ... on AudioAnalysisV6Finished {{
#                     result {{
#                         genre {{
#                             {genres}
#                         }}
#                         mood {{
#                             {moods}
#                         }}
#                     }}
#                 }}
#             }}
#         }}
#     }}
# }}
# """
# results = query_and_get_results(endpoint, query, headers)
# pretty_results = json.dumps(results, indent=2)
# print(pretty_results)

### Keyword search ###


def _get_spotify_ids_from_keyword_search(response):
    edges = response["data"]["keywordSearch"]["edges"]
    return [edge["node"]["id"] for edge in edges]


query = f"""
query KeywordSearchQuery {{
    keywordSearch(
        target: {{ spotify: {{}} }}
        keywords: [
        {{ keyword: "sad", weight: 1 }}
        ]
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
results = query_and_get_results(endpoint, query, headers)
spotify_ids = _get_spotify_ids_from_keyword_search(results)
print(spotify_ids)

### Get all available keywords ###

# def _get_keywords_from_response(response):
#     edges = response["data"]["keywords"]["edges"]
#     return [edge["node"]["keyword"] for edge in edges]

# query = f"""
# {{
#     keywords {{
#         edges {{
#             node {{
#                 keyword
#             }}
#         }}
#     }}
# }}
# """
# results = query_and_get_results(endpoint, query, headers)
# pretty_results = json.dumps(results, indent=2)
# print(pretty_results)
