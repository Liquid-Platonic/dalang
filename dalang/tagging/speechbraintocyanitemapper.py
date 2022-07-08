from dalang.tagging import MappingDict
from dalang.tagging.tagmapper import TagMapper

SPEECHBRAIN_TO_CYANITE_MOODS = {
    "anger": "angry",
    "hap": "happy",
    "sad": "sad",
    # no mapping for neutral
}


class SpeechbrainToCyaniteMapper(TagMapper):
    @property
    def mapping(self) -> MappingDict:
        return SPEECHBRAIN_TO_CYANITE_MOODS
