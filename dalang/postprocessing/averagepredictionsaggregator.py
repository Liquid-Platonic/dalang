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

        for index, prediction in enumerate(predictions):
            weight = 1000 - index * 10
            if weight < 0:
                weight = 0.0
            total_weights += weight
            prediction.update((x, y * weight) for x, y in prediction.items())

        for prediction in predictions:
            prediction.update(
                (x, y / total_weights) for x, y in prediction.items()
            )

        return merge_list_of_dicts_by_average(predictions)
