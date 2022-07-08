from pprint import pprint

from dalang.models.cyanite import Cyanite

spotify_ids = ["7iQM9DQUFKUSNjVt8GQZV2", "5wlucpKdVg0HhVK8oTp7fP"]

id_tags = Cyanite().predict(spotify_ids)

pprint(id_tags)
