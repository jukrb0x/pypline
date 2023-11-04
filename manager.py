import json

from interface import JobInterface
from job_registry import job_registry
from utils import import_job


class PipelineManager:
    def __init__(self, config_file=None, atomics=None) -> None:
        self.jobs = []  # instanced jobs
        self.atomics = atomics if atomics is not None else {}  # atomic variables that shared in the pipeline
        self.config_file = config_file
        self.config_jobs = {}
        self.job_classes_in_config = []  # we use job registry for store, just leave it here for now
        if len(self.jobs) == 0 and self.config_file:
            self.__read_config()
            self.job_classes_in_config = [import_job(w) for w in self.config_jobs]

    def add_registered_jobs(self):
        for job_class in job_registry:
            if issubclass(job_class, JobInterface):
                self.jobs.append(job_class())
            else:
                raise TypeError(f"Job {job_class.__class__.__name__} must implement JobInterface")

    def execute_jobs(self, *parameters):
        if len(self.jobs) == 0:
            print("ERROR: no managed jobs, you may want to `add_registered_jobs` first.")
        for job in self.jobs:
            job.do(*parameters, atomics=self.atomics)
        return [job.__class__.__name__ for job in self.jobs]

    def __read_config(self):
        try:
            with open(self.config_file, "r") as f:
                try:
                    config_object = json.load(f)
                    if not isinstance(config_object, dict):
                        raise Exception("Pipeline config is not a valid json object")
                    self.config_jobs = config_object["jobs"]
                    if not isinstance(self.config_jobs, list):
                        raise Exception(f"[{self.config_file}] Jobs should be a list")
                    atomics = config_object["atomics"]
                    if not isinstance(atomics, dict):
                        raise Exception(f"[{self.config_file}] Atomics should be a dict object")
                    else:
                        # the atomics in the config file has higher priority than manager constructor argument
                        self.atomics = {**self.atomics, **config_object["atomics"]}
                except Exception as e:
                    print("ERROR: failed to load pipeline pipeline config.")
                    print(e)

        except FileNotFoundError:
            print("ERROR: PIPELINE CONFIG NOT FOUND.")
