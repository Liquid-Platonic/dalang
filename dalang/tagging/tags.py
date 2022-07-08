from enum import Enum, auto


class ExtendedEnum(Enum):
    @classmethod
    def to_list(cls):
        return [item.name for item in cls]


class CyaniteMoods(ExtendedEnum):
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


class CyaniteGenres(ExtendedEnum):
    ambient = auto()
    blues = auto()
    classical = auto()
    electronicDance = auto()
    folkCountry = auto()
    jazz = auto()
    funkSoul = auto()
    latin = auto()


class SpeechbrainMoods(ExtendedEnum):
    neutral = auto()
    anger = auto()
    hap = auto()
    sad = auto()


class DistilbertMoods(ExtendedEnum):
    sadness: auto()
    joy: auto()
    love: auto()
    anger: auto()
    fear: auto()
    surprise: auto()
