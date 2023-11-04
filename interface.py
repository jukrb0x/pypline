from abc import ABC, abstractmethod
from job_registry import job_registry


class JobInterface(ABC):
    @abstractmethod
    def do(self, asset_data, *parameters):
        pass

    def __init_subclass__(cls, **kwargs) -> None:
        """
        automatically add Worker class to registry
        """
        super().__init_subclass__(**kwargs)
        job_registry.append(cls)
