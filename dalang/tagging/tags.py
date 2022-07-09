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
    sadness = auto()
    joy = auto()
    love = auto()
    anger = auto()
    fear = auto()
    surprise = auto()


class UserInputMoods(ExtendedEnum):
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
    neutral = auto()
    anger = auto()
    joy = auto()
    love = auto()
    fear = auto()
    shock = auto()


class UserInputGenres(Enum):
    ambient = "ambient"
    blues = "blues"
    classical = "classical"
    dance_electronica = "dance electronica"
    folk_country = "folk country"
    jazz = "jazz"
    soul_funk = "soul funk"
    latin = "latin"

    @classmethod
    def to_list(cls):
        return [item.value for item in cls]
