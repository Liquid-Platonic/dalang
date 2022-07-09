from typing import List

from dalang.helpers import merge_list_of_dicts_by_average
from dalang.postprocessing.predictionsaggregator import PredictionsAggregator
from dalang.tagging import TagPredictions


class AveragePredictionsAggregator(PredictionsAggregator):
    @staticmethod
    def aggregate(predictions: List[TagPredictions]) -> TagPredictions:
        return (
            merge_list_of_dicts_by_average(predictions)
            if predictions
            else None
        )
