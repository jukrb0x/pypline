import json

from worker_registry import worker_registry
from utils import import_worker


class Manager:
    def __init__(self, config_file=None) -> None:
        self.workers = []  # instanced workers
        self.config_file = config_file
        self.config_workers = {}
        self.worker_classes = []  # we use worker registry for store, just leave it here for now
        if len(self.workers) == 0 and self.config_file:
            self.__read_config()
            self.worker_classes = [import_worker(w) for w in self.config_workers]

    def add_registered_workers(self):
        for worker_class in worker_registry:
            self.workers.append(worker_class())

    def execute_workers(self, asset_data, *parameters):
        if len(self.workers) == 0:
            print("ERROR: no managed workers, you may want to `add_registered_workers` first.")
        for worker in self.workers:
            worker.do(asset_data, *parameters)
        return [worker.__class__.__name__ for worker in self.workers]

    def __read_config(self):
        try:
            with open(self.config_file, "r") as f:
                try:
                    self.config_workers = json.load(f)["workers"]
                except Exception as e:
                    print("ERROR: failed to load worker config.")
                    print(e)

        except FileNotFoundError:
            print("ERROR: WORKER CONFIG NOT FOUND.")
