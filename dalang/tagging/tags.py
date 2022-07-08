from enum import Enum, auto


class TagsEnum(Enum):
    @classmethod
    def to_list(cls):
        return [item.name for item in cls]


class CyaniteMoods(TagsEnum):
    aggressive = auto()
    calm = auto()
    chilled = auto()
    dark = auto()
    energetic = auto()
    epic = auto()
    happy = auto()
    romantic = auto()
    sad = auto()
    scary = auto()
    sexy = auto()
    ethereal = auto()
    uplifting = auto()


class CyaniteGenres(TagsEnum):
    ambient: auto()
    blues: auto()
    classical: auto()
    electronicDance: auto()
    folkCountry: auto()
    jazz: auto()
    funkSoul: auto()
    latin: auto()


class SpeechbrainMoods(TagsEnum):
    neutral: auto()
    anger: auto()
    hap: auto()
    sad: auto()


class DistilbertMoods(TagsEnum):
    sadness: auto()
    joy: auto()
    love: auto()
    anger: auto()
    fear: auto()
    surprise: auto()
