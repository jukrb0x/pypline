import unittest
from manager import PipelineManager
from interface import JobInterface


class TestJobA(JobInterface):
    def do(self, *parameters, atomics):
        atomics['name'] = "Changed In A"
        print(f"[{self.__class__.__name__}] atomics: {atomics}, parameters: {parameters}")


class TestJobB(JobInterface):
    def do(self, *parameters, atomics):
        print(f"[{self.__class__.__name__}] atomics: {atomics}, parameters: {parameters}")


class TestManager(unittest.TestCase):
    def test_add_registered_jobs(self):
        manager = PipelineManager()
        manager.add_registered_jobs()
        self.assertEqual(len(manager.jobs), 2)

    def test_execute_jobs(self):
        atomics = {'name': 'joe', 'asset_data': ["/Game/A", "/Game/B"]}
        manager = PipelineManager(atomics=atomics)
        parameters = (1, 2, "some_string", 1.234, ['element'], ('a', 'b'), {'k': 'v'})
        manager.add_registered_jobs()
        executed_jobs = manager.execute_jobs(parameters)
        self.assertEqual(executed_jobs, ["TestJobA", "TestJobB"])


if __name__ == "__main__":
    unittest.main()
