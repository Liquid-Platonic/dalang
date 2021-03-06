from typing import Dict, List

from transformers import pipeline

from dalang.models.huggingfacemodel import HuggingFaceModel
from dalang.tagging import TagPredictions
from dalang.tagging.distilberttokeywordsmapper import (
    DistilbertToKeywordsMapper,
)


class Text2Mood(HuggingFaceModel):
    def __init__(self, tag_mapper: DistilbertToKeywordsMapper) -> None:
        super().__init__(tag_mapper)

    def _get_raw_model(self) -> None:
        self.raw_model = pipeline(
            "text-classification",
            model="bhadresh-savani/distilbert-base-uncased-emotion",
            return_all_scores=True,
        )

    def predict(self, text: str) -> TagPredictions:
        prediction = self.raw_model(text)
        prediction = self._convert_list_of_dicts_to_dict(prediction)
        return self.tag_mapper.map(prediction)

    def predict_batch(self, texts: List[str]) -> List[TagPredictions]:
        output = []
        for text in texts:
            try:
                output.append(self.predict(text))
            except:
                pass
        return output

    @staticmethod
    def _convert_list_of_dicts_to_dict(
        list_of_dicts: List[Dict[str, float]]
    ) -> TagPredictions:
        return {dict_["label"]: dict_["score"] for dict_ in list_of_dicts}
