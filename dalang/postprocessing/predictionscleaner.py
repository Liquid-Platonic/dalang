from typing import List

from dalang.tagging import TagPredictions
from dalang.utils import is_result_dict_valid


class PredictionsCleaner:
    def __init__(self, threshold: float) -> None:
        self.threshold = threshold

    def clean(self, predictions: List[TagPredictions]) -> List[TagPredictions]:
        return list(
            filter(
                lambda prediction: is_result_dict_valid(
                    prediction, self.threshold
                ),
                predictions,
            )
        )
