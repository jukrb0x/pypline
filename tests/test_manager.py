import unittest
from manager import Manager
from interface import WorkerInterface


class TestWorkerA(WorkerInterface):
    def do(self, asset_data, *parameters):
        print(f"[{self.__class__.__name__}] asset data: {asset_data}, parameters: {parameters}")


class TestWorkerB(WorkerInterface):
    def do(self, asset_data, *parameters):
        print(f"[{self.__class__.__name__}] asset data: {asset_data}, parameters: {parameters}")


class TestManager(unittest.TestCase):
    def test_add_registered_workers(self):
        manager = Manager()
        manager.add_registered_workers()
        self.assertEqual(len(manager.workers), 2)

    def test_execute_workers(self):
        manager = Manager()
        asset_data = ["/Game/A", "/Game/B"]
        parameters = (1, 2, "some_string", 1.234, ['element'], ('a', 'b'), {'k': 'v'})
        manager.add_registered_workers()
        executed_workers = manager.execute_workers(asset_data, parameters)
        self.assertEqual(executed_workers, ["TestWorkerA", "TestWorkerB"])


if __name__ == "__main__":
    unittest.main()
