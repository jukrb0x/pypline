from manager import Manager

from workers import worker_a

manager = Manager()

manager.add_registered_workers()

asset_data = ["test"]

parameters = (1,2)

manager.execute_workers(asset_data, *parameters)
