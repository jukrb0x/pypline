import importlib


def import_job(worker_config):
    module_name = worker_config["module"]
    class_name = worker_config["class"]
    module = importlib.import_module(module_name)
    worker_class = getattr(module, class_name)
    return worker_class
