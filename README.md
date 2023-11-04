# Pypline

Python Script As Pipeline

## How to use

### Imported worker manually

All concreate classes of `WorkerInterface` in `worker_a` and `worker_b` will be automatically added into worker registry
when they are imported in the script.

**main.py**

```python
from manager import Manager
from workers import worker_a, worker_b

manager = Manager()
manager.add_registered_workers()

asset_data = ["/Game/A", "/Game/B"]
parameters = (1, 2, "some_string", 1.234, ['element'], ('a', 'b'), {'k': 'v'})

manager.execute_workers(asset_data, *parameters)
```

### Automated with worker config

Execute workers with a workers config json file, which allows more flexible way to specify the module and
exact `WorkerInterface` classes.

**workers.json**

```json
{
  "workers": [
    {
      "module": "workers.worker_a",
      "class": "WorkerA"
    },
    {
      "module": "workers.worker_b",
      "class": "SomeNamedWorker"
    }
  ]
}
```

**main.py**

```python
from manager import Manager
import pathlib

manager = Manager(pathlib.Path(__file__).parent / "workers.json")
manager.add_registered_workers()

asset_data = ["/Game/A", "/Game/B"]
parameters = (1, 2, "some_string", 1.234, ['element'], ('a', 'b'), {'k': 'v'})

manager.execute_workers(asset_data, *parameters)
```

Both of usage should give the output as following:

```shell
$ python main.py

[WorkerA] asset data: ['/Game/A', '/Game/B'], parameters: (1, 2, 'some_string', 1.234, ['element'], ('a', 'b'), {'k': 'v'})
[SomeNamedWorker] asset data: ['/Game/A', '/Game/B'], parameters: (1, 2, 'some_string', 1.234, ['element'], ('a', 'b'), {'k': 'v'})
```

## Tests

```shell
python -m uniitest discover
```