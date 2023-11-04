import json

from worker_registry import worker_registry
from utils import import_worker


class Manager:
    def __init__(self, config_file=None) -> None:
        self.workers = []
        self.config_file = config_file
        self.config_workers = {}
        if len(self.workers) == 0 and self.config_file:
            self.__read_config()
            for c in self.config_workers:
                import_worker(c)

    def add_registered_workers(self):
        for worker_class in worker_registry:
            self.workers.append(worker_class())

    def execute_workers(self, asset_data, *parameters):
        for worker in self.workers:
            worker.do(asset_data, *parameters)

    def __read_config(self):
        try:
            with open(self.config_file, "r") as f:
                try:
                    self.config_workers = json.load(f)["workers"]
                except Exception as e:
                    print("ERROR: failed to load worker config.")
                    print(e)

        except FileNotFoundError:
            print("ERROR: WORKER CONFIG NOT FOUND")
