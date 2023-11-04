from manager import Manager

manager = Manager()

manager.add_registered_workers()

asset_data = ["/Game/A", "/Game/B"]

parameters = (1, 2, "some_string")

manager.execute_workers(asset_data, *parameters)
