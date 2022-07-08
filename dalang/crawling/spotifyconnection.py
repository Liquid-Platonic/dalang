from typing import Optional

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyConnection:
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.spotify_connection: Optional[spotipy.Spotify] = None
        self._get_spotify_connection(client_id, client_secret)

    def __call__(self):
        return self.spotify_connection

    def _get_spotify_connection(
        self, client_id: str = None, client_secret: str = None
    ) -> None:
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id, client_secret=client_secret
        )
        self.spotify_connection = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager
        )
