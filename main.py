from manager import PipelineManager
import pathlib

manager = PipelineManager(pathlib.Path(__file__).parent / "pipeline.json")
manager.add_registered_jobs()

# todo: pass asset data and parameters from somewhere else
asset_data = ["/Game/A", "/Game/B"]
parameters = (1, 2, "some_string", 1.234, ['element'], ('a', 'b'), {'k': 'v'})

manager.execute_jobs(asset_data, *parameters)
