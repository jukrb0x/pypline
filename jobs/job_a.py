from interface import JobInterface


class JobA(JobInterface):
    def do(self, *parameters, atomics):
        print(f"[{self.__class__.__name__}] atomics: {atomics}, parameters: {parameters}")
        atomics['name'] = "Homer Simpson"
