from abc import ABC, abstractmethod
from worker_registry import worker_registry


class WorkerInterface(ABC):
    @abstractmethod
    def do(self, asset_data, *parameters):
        pass

    def __init_subclass__(cls, **kwargs) -> None:
        """
        automatically add Worker class to registry
        """
        super().__init_subclass__(**kwargs)
        worker_registry.append(cls)
