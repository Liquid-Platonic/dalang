from pprint import pprint

from dalang.models import cyanite_model

spotify_ids = ["7iQM9DQUFKUSNjVt8GQZV2", "5wlucpKdVg0HhVK8oTp7fP"]

id_tags = cyanite_model.predict(spotify_ids)

pprint(id_tags)
