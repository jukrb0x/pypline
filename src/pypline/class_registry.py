class ClassRegistry:
    """
    In Unreal Engine or some case, the Python environment is persistent, we need to use this registry class to ensure
    the unique element after module hot reloading
    """

    def __init__(self):
        self._registry = {}

    def add(self, cls):
        """
        add only if they have the different module name and class name
        """
        key = f"{cls.__module__}.{cls.__name__}"
        if key not in self._registry:
            self._registry[key] = cls

    def __contains__(self, cls):
        key = f"{cls.__module__}.{cls.__name__}"
        return key in self._registry

    def __iter__(self):
        return iter(self._registry.values())

    def __len__(self):
        return len(self._registry)

    def __repr__(self):
        return f"ClassRegistry({list(self._registry.values())})"

    def clear(self):
        self._registry = {}

    def get_registry(self):
        return self._registry
