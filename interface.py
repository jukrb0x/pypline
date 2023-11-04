from abc import abstractmethod
from worker_registry import worker_registry


class WorkerInterface():
    @abstractmethod
    def do(self, asset_data, *parameters):
        pass

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        worker_registry.append(cls)
