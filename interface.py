from abc import ABC, abstractmethod
from job_registry import job_registry
from inspect import signature


class JobInterface(ABC):
    @abstractmethod
    def do(self, *parameters, atomics):
        pass

    def __init_subclass__(cls, **kwargs) -> None:
        """
        automatically add Worker class to registry
        """
        super().__init_subclass__(**kwargs)

        # check method signature
        abstract_signature_of_do = signature(JobInterface.do)
        concrete_signature_of_do = signature(cls.do)

        if abstract_signature_of_do != concrete_signature_of_do:
            raise TypeError(
                f"The method {cls.do.__name__} in class {cls.__name__} must have the same signature as the abstract method: {abstract_signature_of_do}")

        job_registry.append(cls)
