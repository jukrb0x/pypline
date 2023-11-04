from interface import WorkerInterface

class WorkerA(WorkerInterface):
    def do(self, asset_data, *parameters):
        print(f"worker a: {asset_data}, parameters: {parameters}")
