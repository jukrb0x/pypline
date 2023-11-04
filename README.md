# Pypline

Python Script As Pipeline

## How to use

### Imported job manually

All concreate classes of `JobInterface` in `job_a` and `job_b` will be automatically added into job registry
when they are imported in the script.

**main.py**

```python
from manager import PipelineManager
from jobs import job_a, job_b

manager = PipelineManager()
manager.add_registered_jobs()

asset_data = ["/Game/A", "/Game/B"]
parameters = (1, 2, "some_string", 1.234, ['element'], ('a', 'b'), {'k': 'v'})

manager.execute_jobs(asset_data, *parameters)
```

### Automated with pipeline config

Execute jobs with a config json file, which allows more flexible way to specify the module and exact `JobInterface`
classes.

**pipeline.json**

```json
{
  "jobs": [
    {
      "module": "jobs.job_a",
      "class": "JobA"
    },
    {
      "module": "jobs.job_b",
      "class": "SomeNamedJob"
    }
  ]
}
```

**main.py**

```python
from manager import PipelineManager
import pathlib

manager = PipelineManager(pathlib.Path(__file__).parent / "pipeline.json")
manager.add_registered_jobs()

asset_data = ["/Game/A", "/Game/B"]
parameters = (1, 2, "some_string", 1.234, ['element'], ('a', 'b'), {'k': 'v'})

manager.execute_jobs(asset_data, *parameters)
```

Both of usage should give the output as following:

```shell
$ python main.py

[JobA] asset data: ['/Game/A', '/Game/B'], parameters: (1, 2, 'some_string', 1.234, ['element'], ('a', 'b'), {'k': 'v'})
[SomeNamedJob] asset data: ['/Game/A', '/Game/B'], parameters: (1, 2, 'some_string', 1.234, ['element'], ('a', 'b'), {'k': 'v'})
```

## Tests

```shell
python -m uniitest discover
```