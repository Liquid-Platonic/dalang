from abc import abstractmethod
from typing import Any, Optional

from dalang.tagging.tagmapper import TagMapper
from dalang.utils.singleton import Singleton


class HuggingFaceModel(metaclass=Singleton):
    def __init__(self, tag_mapper: Optional[TagMapper] = None):
        self.tag_mapper = tag_mapper
        self.raw_model: Optional[Any] = None
        self._get_raw_model()

    @abstractmethod
    def _get_raw_model(self) -> None:
        pass
