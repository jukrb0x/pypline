import unittest
from manager import PipelineManager
from interface import JobInterface


class TestJobA(JobInterface):
    def do(self, asset_data, *parameters, atomics):
        atomics['name'] = "Name Changed In A"
        print(f"[{self.__class__.__name__}] asset data: {asset_data}, parameters: {parameters}, atomics: {atomics}")


class TestJobB(JobInterface):
    def do(self, asset_data, *parameters, atomics):
        print(f"[{self.__class__.__name__}] asset data: {asset_data}, parameters: {parameters}, atomics: {atomics}")


class TestManager(unittest.TestCase):
    def test_add_registered_jobs(self):
        manager = PipelineManager()
        manager.add_registered_jobs()
        self.assertEqual(len(manager.jobs), 2)

    def test_execute_jobs(self):
        manager = PipelineManager()
        asset_data = ["/Game/A", "/Game/B"]
        parameters = (1, 2, "some_string", 1.234, ['element'], ('a', 'b'), {'k': 'v'})
        atomics = {'name': 'joe'}
        manager.add_registered_jobs()
        executed_jobs = manager.execute_jobs(asset_data, parameters)
        self.assertEqual(executed_jobs, ["TestJobA", "TestJobB"])


if __name__ == "__main__":
    unittest.main()
