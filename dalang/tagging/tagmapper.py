from abc import abstractmethod

from dalang.helpers import map_dict_keys
from dalang.tagging import MappingDict, TagPredictions


class TagMapper:
    @property
    @abstractmethod
    def mapping(self) -> MappingDict:
        pass

    def map(self, tag_predictions: TagPredictions) -> TagPredictions:
        return map_dict_keys(tag_predictions, self.mapping)
