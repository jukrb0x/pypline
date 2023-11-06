from pypline import JobInterface


class JobB(JobInterface):
    def do(self, *parameters, atomics):
        print(f"[{self.__class__.__name__}] atomics: {atomics}, parameters: {parameters}")
