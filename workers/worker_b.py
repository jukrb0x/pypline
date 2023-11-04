from interface import WorkerInterface


class SomeNamedWorker(WorkerInterface):
    def do(self, asset_data, *parameters):
        print(f"[{self.__class__.__name__}] asset data: {asset_data}, parameters: {parameters}")
