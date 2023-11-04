from manager import PipelineManager
import pathlib

atomics = {'asset_data': ["/Game/A", "/Game/B"]}
manager = PipelineManager(config_file=pathlib.Path(__file__).parent / "pipeline.json", atomics=atomics)
manager.add_registered_jobs()

# todo: pass asset data and parameters from somewhere else
parameters = (1, 2, "some_string", 1.234, ['element'], ('a', 'b'), {'k': 'v'})

manager.execute_jobs(*parameters)
