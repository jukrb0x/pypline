"""
TODO: Example File
"""

# Static Modules
import pathlib
import pypline
from pypline import Pipeline, in_unreal_engine, remove_package

# Hot-reloaded Modules for Unreal Engine
if in_unreal_engine():
    # this will invoke a full pacakge imports
    remove_package(pypline)

    from pypline import Pipeline


def run():
    # >>> hot reload a module >>>
    # import my_job
    # hotreload_module(my_job)
    # a = Pipeline()
    # <<< hot reload a module <<<

    a = Pipeline(pathlib.Path(__file__).parent / "pipeline.json")

    a.add_registered_jobs()
    a.execute_jobs()


if __name__ == "__main__":
    run()
