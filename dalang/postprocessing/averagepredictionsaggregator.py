from collections import defaultdict
from typing import List

from dalang.helpers import merge_dicts, merge_list_of_dicts_by_average
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

    @staticmethod
    def aggregate_linear(predictions):
        if not predictions:
            return None

        total_weights = 0
        sum_vector = defaultdict(float)
        for index, prediction in enumerate(predictions):
            weight = 1000 - index * 100
            if weight < 0:
                weight = 0.0
            total_weights += weight

            for x, y in prediction.items():
                sum_vector[x] += y * weight

        sum_vector.update(
            (x, y / total_weights) for x, y in sum_vector.items()
        )

        return sum_vector
