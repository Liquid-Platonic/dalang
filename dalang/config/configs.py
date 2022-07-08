import os
from pathlib import Path

from dotenv import load_dotenv

dotenv_path = Path(__file__).parent / "config.env"
load_dotenv(dotenv_path)

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
PORT = os.environ.get("PORT")
API_URL = os.environ.get("API_URL")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
