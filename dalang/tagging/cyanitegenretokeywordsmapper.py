from dalang.tagging import MappingDict
from dalang.tagging.tagmapper import TagMapper

CYANITE_GENRES_TO_CYANITE_KEYWORDS = {
    "funkSoul": "soul funk",
    "electronicDance": "dance electronica",
    "folkCountry": "country folk",
}


class CyaniteGenreToKeywordsMapper(TagMapper):
    @property
    def mapping(self) -> MappingDict:
        return CYANITE_GENRES_TO_CYANITE_KEYWORDS
