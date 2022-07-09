from pathlib import Path
from typing import List

import torch
from speechbrain.pretrained.interfaces import foreign_class

from dalang.models.huggingfacemodel import HuggingFaceModel
from dalang.tagging import TagPredictions
from dalang.tagging.speechbraintokeywordsmapper import (
    SpeechbrainToKeywordsMapper,
)
from dalang.tagging.tags import SpeechbrainMoods


class Speechbrain(HuggingFaceModel):
    def __init__(self, tag_mapper: SpeechbrainToKeywordsMapper = SpeechbrainToKeywordsMapper()):
        super().__init__(tag_mapper)

    def _get_raw_model(self) -> None:
        self.raw_model = foreign_class(
            source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
            pymodule_file="custom_interface.py",
            classname="CustomEncoderWav2vec2Classifier",
        )

    def predict(self, audio_path: Path) -> TagPredictions:
        predictions, _, _, _ = self.raw_model.classify_file(audio_path.as_posix())
        predictions = self._convert_torch_tensor_to_tag_prediction(predictions)
        return self.tag_mapper.map(predictions)

    def predict_batch(self, audio_paths: List[Path]) -> List[TagPredictions]:
        return [self.predict(audio_path) for audio_path in audio_paths]

    def _convert_torch_tensor_to_tag_prediction(self, tensor: torch.Tensor) -> TagPredictions:
        return dict(zip(SpeechbrainMoods.to_list(), tensor[0].tolist()))
