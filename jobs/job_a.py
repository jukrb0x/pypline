from interface import JobInterface


class JobA(JobInterface):
    def do(self, asset_data, *parameters, atomics):
        print(f"[{self.__class__.__name__}] asset data: {asset_data}, parameters: {parameters}")
