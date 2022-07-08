from dalang.tagging import MappingDict
from dalang.tagging.tagmapper import TagMapper

DISTILBERT_TO_CYANITE_MOODS = {
    "sadness": "sad",
    "joy": "joyful",
    "love": "loving",
    "anger": "angry",
    "fear": "fearful",
    # no mapping for surprise
}


class DistilbertToCyaniteMapper(TagMapper):
    @property
    def mapping(self) -> MappingDict:
        return DISTILBERT_TO_CYANITE_MOODS
