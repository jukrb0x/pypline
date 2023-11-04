import json

from job_registry import job_registry
from utils import import_job


class PipelineManager:
    def __init__(self, config_file=None) -> None:
        self.jobs = []  # instanced jobs
        self.config_file = config_file
        self.config_jobs = {}
        self.job_classes = []  # we use job registry for store, just leave it here for now
        if len(self.jobs) == 0 and self.config_file:
            self.__read_config()
            self.job_classes = [import_job(w) for w in self.config_jobs]

    def add_registered_jobs(self):
        for job_class in job_registry:
            self.jobs.append(job_class())

    def execute_jobs(self, asset_data, *parameters):
        if len(self.jobs) == 0:
            print("ERROR: no managed jobs, you may want to `add_registered_jobs` first.")
        for job in self.jobs:
            job.do(asset_data, *parameters)
        return [job.__class__.__name__ for job in self.jobs]

    def __read_config(self):
        try:
            with open(self.config_file, "r") as f:
                try:
                    self.config_jobs = json.load(f)["jobs"]
                except Exception as e:
                    print("ERROR: failed to load pipeline pipeline config.")
                    print(e)

        except FileNotFoundError:
            print("ERROR: PIPELINE CONFIG NOT FOUND.")
