from pathlib import Path
from typing import List, Tuple

import librosa
import numpy as np
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

from dalang.models.huggingfacemodel import HuggingFaceModel


class Speech2Text(HuggingFaceModel):
    def __init__(self) -> None:
        self._get_processor()
        super().__init__()

    def _get_raw_model(self) -> None:
        self.raw_model = Wav2Vec2ForCTC.from_pretrained(
            "facebook/wav2vec2-base-960h"
        )

    def _load_audio(self, audio_path: Path) -> Tuple[np.ndarray, int]:
        audio, sr = librosa.load(audio_path.as_posix(), sr=16000)
        return audio, sr

    def _get_processor(self) -> None:
        self.processor = Wav2Vec2Processor.from_pretrained(
            "facebook/wav2vec2-base-960h"
        )

    def predict(self, audio_path: Path) -> str:
        audio, sr = self._load_audio(audio_path)
        input_values = self.processor(
            audio, return_tensors="pt", padding="longest", sampling_rate=sr
        ).input_values
        logits = self.raw_model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        prediction = self.processor.batch_decode(predicted_ids)
        return prediction

    def predict_batch(self, audio_paths: List[Path]) -> List[str]:
        return [self.predict(audio_path) for audio_path in audio_paths]


speech_to_text_model = Speech2Text()
