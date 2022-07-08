from dalang.tagging import MappingDict
from dalang.tagging.tagmapper import TagMapper

SPEECHBRAIN_MOODS_TO_CYANITE_KEYWORDS = {
    "hap": "happy",
}


class SpeechbrainToKeywordsMapper(TagMapper):
    @property
    def mapping(self) -> MappingDict:
        return SPEECHBRAIN_MOODS_TO_CYANITE_KEYWORDS
