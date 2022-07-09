from dalang.models.cyanite import Cyanite
from dalang.models.speechtomood import Speech2Mood
from dalang.models.texttomood import Text2Mood
from dalang.tagging.distilberttokeywordsmapper import (
    DistilbertToKeywordsMapper,
)
from dalang.tagging.speechbraintokeywordsmapper import (
    SpeechbrainToKeywordsMapper,
)

cyanite_model = Cyanite()
speech_to_mood_model = Speech2Mood(SpeechbrainToKeywordsMapper())
text_to_mood_model = Text2Mood(DistilbertToKeywordsMapper())
