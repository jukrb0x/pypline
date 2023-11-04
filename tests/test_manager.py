import pathlib
import unittest
from pypline import Pipeline
from interface import JobInterface


class TestJobA(JobInterface):
    def do(self, *parameters, atomics):
        print(f"[{self.__class__.__name__}] atomics: {atomics}, parameters: {parameters}")
        atomics['name'] = "Changed In A"


class TestJobB(JobInterface):
    def do(self, *parameters, atomics):
        print(f"[{self.__class__.__name__}] atomics: {atomics}, parameters: {parameters}")


class TestManager(unittest.TestCase):
    def test_add_registered_jobs(self):
        manager = Pipeline()
        manager.add_registered_jobs()
        self.assertEqual(len(manager.jobs), 2)

    def test_execute_jobs(self):
        atomics = {'name': 'Joe', 'asset_data': ["/Game/A", "/Game/B"]}
        manager = Pipeline(atomics=atomics)
        parameters = (1, 2, "some_string", 1.234, ['element'], ('a', 'b'), {'k': 'v'})
        manager.add_registered_jobs()
        executed_jobs = manager.execute_jobs(parameters)
        self.assertEqual(["TestJobA", "TestJobB"], executed_jobs)

    def test_execute_jobs_with_config(self):
        atomics = {'name': 'Joe', 'asset_data': ["/Game/A", "/Game/B"]}
        manager = Pipeline(config_file=pathlib.Path(__file__).parent / "pipeline.json", atomics=atomics)
        parameters = (1, 2, "some_string", 1.234, ['element'], ('a', 'b'), {'k': 'v'})
        manager.add_registered_jobs()
        executed_jobs = manager.execute_jobs(parameters)
        self.assertEqual(["TestJobA", "TestJobB", "JobA", "JobB"], executed_jobs)


if __name__ == "__main__":
    unittest.main()
