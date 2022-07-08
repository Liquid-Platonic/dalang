import sys

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

search_str = "squarepusher - my red hot car"

client_credentials_manager = SpotifyClientCredentials(
    client_id="82fcc995730641ad9cd9357aa453429d",
    client_secret="ab99805e1d78483889105cbfbb2d18ee",
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Search track by song title and get spotify id
result = sp.search(search_str)
spotify_id = result["tracks"]["items"][0]["id"]
print(spotify_id)

# Recommend songs from spotify track ids
recommendations = sp.recommendations(seed_tracks=[spotify_id], limit=10)
spotify_ids = [
    (track["id"], track["artists"][0]["name"], track["name"])
    for track in recommendations["tracks"]
]
print(spotify_ids)
