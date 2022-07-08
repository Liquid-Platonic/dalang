from dalang.apis.cyaniteapi import CyaniteApi

cyanite_api = CyaniteApi()

spotify_id = "7iQM9DQUFKUSNjVt8GQZV2"
genres, moods = cyanite_api.get_moods_and_genres(spotify_id)
print("genres", genres)
print("moods", moods)

keywords = {"happy": 1, "ambient": 1}
spotify_ids = cyanite_api.get_spotify_ids_by_keywords(keywords)
print(spotify_ids)
