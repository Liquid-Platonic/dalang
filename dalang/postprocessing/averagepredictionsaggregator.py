from typing import List

from dalang.postprocessing.predictionsaggregator import PredictionsAggregator
from dalang.tagging import TagPredictions
from dalang.utils import merge_list_of_dicts_by_average


class AveragePredictionsAggregator(PredictionsAggregator):
    @staticmethod
    def aggregate(predictions: List[TagPredictions]) -> TagPredictions:
        return merge_list_of_dicts_by_average(predictions)
