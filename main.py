from manager import PipelineManager
import pathlib

asset_data = ["/Game/C"]
ext_atomics = {'asset_data': asset_data}
pipeline_config_file = pathlib.Path(__file__).parent / "pipeline.json"

if __name__ == "__main__":
    manager = PipelineManager(config_file=pipeline_config_file, atomics=ext_atomics)
    manager.add_registered_jobs()

    parameters = (1, 2, "some_string", 1.234, ['element'], ('a', 'b'), {'k': 'v'})

    manager.execute_jobs(*parameters)
