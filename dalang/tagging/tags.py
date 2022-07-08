from dalang.apis.utils import get_genres, get_moods, get_moods_advanced
from dalang.config.config import ACCESS_TOKEN, API_URL

endpoint = API_URL
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

CYANITE_MOODS = get_moods(endpoint, headers)[:-1]
CYANITE_MOODS_ADVANCED = get_moods_advanced(endpoint, headers)
CYANITE_GENRES = get_genres(endpoint, headers)
SPEECHBRAIN_MOODS = ["neutral", "anger", "hap", "sad"]
DISTILBERT_MOODS = ["sadness", "joy", "love", "anger", "fear", "surprise"]
