import sys

from dalang.apis.spotify import SpotifyApi

search_str = "squarepusher - my red hot car"

spotify_api = SpotifyApi()

spotify_api.get_spotify_id_by_yt_title(search_str)
spotify_id = result["tracks"]["items"][0]["id"]
print(spotify_id)

# Recommend songs from spotify track ids
recommendations = sp.recommendations(seed_tracks=[spotify_id], limit=10)
spotify_ids = [
    (track["id"], track["artists"][0]["name"], track["name"]) for track in recommendations["tracks"]
]
print(spotify_ids)
