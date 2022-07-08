from dalang.tagging import MappingDict
from dalang.tagging.tagmapper import TagMapper

DISTILBERT_MOODS_TO_CYANITE_KEYWORDS = {"sadness": "sad", "surprise": "shock"}


class DistilbertToKeywordsMapper(TagMapper):
    @property
    def mapping(self) -> MappingDict:
        return DISTILBERT_MOODS_TO_CYANITE_KEYWORDS
