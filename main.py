from manager import Manager
import pathlib

manager = Manager(pathlib.Path(__file__).parent / "worker.json")
manager.add_registered_workers()

# todo: pass asset data and parameters from somewhere else
asset_data = ["/Game/A", "/Game/B"]
parameters = (1, 2, "some_string", 1.234, ['element'], ('a', 'b'), {'k': 'v'})

manager.execute_workers(asset_data, *parameters)
