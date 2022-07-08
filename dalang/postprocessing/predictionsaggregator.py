from abc import ABC
from typing import List

from dalang.tagging import TagPredictions


class PredictionsAggregator(ABC):
    @staticmethod
    def aggregate(predictions: List[TagPredictions]) -> TagPredictions:
        pass
