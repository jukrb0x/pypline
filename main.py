from manager import Manager
import pathlib
import json
from utils import import_worker

# with open(pathlib.Path(__file__).parent / "worker.json") as f:
#     wks = json.load(f)["workers"]
# for wk in wks:
#     import_worker(wk)

manager = Manager(pathlib.Path(__file__).parent / "worker.json")
manager.add_registered_workers()

asset_data = ["/Game/A", "/Game/B"]

parameters = (1, 2, "some_string")

manager.execute_workers(asset_data, *parameters)
