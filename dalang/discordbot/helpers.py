import re

import nltk

from dalang.helpers import get_top_dict_items, merge_dicts
from dalang.tagging import TagPredictions

english_words = set(nltk.corpus.words.words())
emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U00002500-\U00002BEF"  # chinese char
    "\U00002702-\U000027B0"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U0001f926-\U0001f937"
    "\U00010000-\U0010ffff"
    "\u2640-\u2642"
    "\u2600-\u2B55"
    "\u200d"
    "\u23cf"
    "\u23e9"
    "\u231a"
    "\ufe0f"  # dingbats
    "\u3030"
    "]+",
    flags=re.UNICODE,
)


def convert_fetched_messages_to_model_input(messages):
    output = []
    for channel in messages:
        info = messages[channel]
        if not info:
            continue
        for message in info:
            output.append(message["message"])
    return " ".join(output)


def batch_string(string, batch_size=1500):
    return [
        string[i : i + batch_size] for i in range(0, len(string), batch_size)
    ]


def clean_string(string):
    string = re.sub(r"[^a-zA-Z0-9 [^{}]+]", "", string)
    string = " ".join(
        w
        for w in nltk.wordpunct_tokenize(string)
        if w.lower() in english_words or not w.isalpha()
    )
    return re.sub(emoji_pattern, "", string)


def prepare_inputs_for_keyword_search(
    genres: TagPredictions, moods: TagPredictions
) -> TagPredictions:
    top_genres = get_top_dict_items(genres, n=3)
    top_moods = get_top_dict_items(moods, n=4)
    return merge_dicts([top_genres, top_moods])
