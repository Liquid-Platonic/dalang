from typing import List

from discord import TextChannel

from dalang.crawling import spotify_id_crawler
from dalang.discordbot.fetch_youtube_links_from_channel import (
    fetch_youtube_links_from_channel,
)
from dalang.models import cyanite_model
from dalang.postprocessing.averagepredictionsaggregator import (
    AveragePredictionsAggregator,
)


async def youtube_to_genre_mood(
    text_channels: List[TextChannel], window_minutes: int = 5
):
    yt_titles = await fetch_youtube_links_from_channel(
        text_channels, window_minutes=window_minutes
    )
    spotify_ids = spotify_id_crawler.get_ids_by_titles(yt_titles)
    if not spotify_ids:
        return {}, {}, []
    cyanite_tags = cyanite_model.predict(spotify_ids)

    genres = {}
    if cyanite_tags["genres"]:
        genres = AveragePredictionsAggregator.aggregate(cyanite_tags["genres"])

    moods = {}
    if cyanite_tags["moods"]:
        moods = AveragePredictionsAggregator.aggregate(cyanite_tags["moods"])

    return genres, moods, spotify_ids
