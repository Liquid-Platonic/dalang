from dalang.models.distilbert import Distilbert
from dalang.models.speechbrain import Speechbrain
from dalang.tagging.distilberttokeywordsmapper import (
    DistilbertToKeywordsMapper,
)
from dalang.tagging.speechbraintokeywordsmapper import (
    SpeechbrainToKeywordsMapper,
)

speech_to_mood_model = Speechbrain(SpeechbrainToKeywordsMapper())
text_to_mood_model = Distilbert(DistilbertToKeywordsMapper())
