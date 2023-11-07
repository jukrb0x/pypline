import importlib
import sys
import pkgutil
from .job_registry import job_registry


def import_job(worker_config, hotreload=False):
    module_name = worker_config["module"]
    class_name = worker_config["class"]

    # Check if the class is already in the job_registry
    # prevent duplicate job classes
    for cls in job_registry:
        if cls.__module__ == module_name and cls.__name__ == class_name:
            return cls

    if module_name in sys.modules:
        if hotreload:
            del sys.modules[module_name]
            module = importlib.import_module(module_name)
        else:
            module = sys.modules[module_name]
    else:
        module = importlib.import_module(module_name)

    job_class = getattr(module, class_name)
    return job_class


def hotreload_module(module):
    """
    used to hot reload a specific module in unreal engine python,
    unreal engine python runtime only ends when editor exists
    """
    module_name = module.__name__
    if module_name in sys.modules:
        del sys.modules[module_name]

    module = importlib.import_module(module_name)
    return module


def hotreload_package(package):
    """
    FIXME: do not use this
    """
    modules_to_reload = []
    for module_name in sys.modules:
        if module_name == package.__name__ or module_name.startswith(str(package.__name__) + "."):
            del sys.modules[module_name]
            modules_to_reload.append(importlib.import_module(module_name))
    return modules_to_reload


def remove_package(package):
    modules_to_remove = []
    for module_name in sys.modules:
        if module_name == package.__name__ or module_name.startswith(str(package.__name__) + "."):
            modules_to_remove.append(module_name)
    for module_name in modules_to_remove:
        del sys.modules[module_name]
    return modules_to_remove


def in_unreal_engine():
    return True if '_unreal_engine' in sys.modules else False
