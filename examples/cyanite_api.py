import json

from dalang.apis.utils import query_and_get_results
from dalang.config.config import ACCESS_TOKEN, API_URL
from dalang.tagging.tags import CYANITE_GENRES, CYANITE_MOODS

endpoint = API_URL
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

spotify_id = "7iQM9DQUFKUSNjVt8GQZV2"

# Get genres & moods
genres = "\n".join(CYANITE_GENRES)
moods = "\n".join(CYANITE_MOODS)
query = f"""
{{
    spotifyTrack(id: "{spotify_id}") {{
        ... on SpotifyTrack {{
            audioAnalysisV6 {{
                ... on AudioAnalysisV6Finished {{
                    result {{
                        genre {{
                            {genres}
                        }}
                        mood {{
                            {moods}
                        }}
                    }}
                }}  
            }}
        }}
    }}
}}
"""

results = query_and_get_results(endpoint, query, headers)
pretty_results = json.dumps(results, indent=2)
print(pretty_results)
