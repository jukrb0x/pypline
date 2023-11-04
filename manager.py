from worker_registry import worker_registry


class Manager:
    def __init__(self) -> None:
        self.workers = []

    def add_registered_workers(self):
        for worker_class in worker_registry:
            self.workers.append(worker_class())

    def execute_workers(self, asset_data, *parameters):
        for worker in self.workers:
            worker.do(asset_data, *parameters)
