# Pypline

Python Script As Pipeline.

A **Pipeline** consists of the different jobs and executes them in the order. A **Job** is an action node in the
pipeline, jobs share pipeline variables called **Atomics** which can be modified by jobs.

## How to use

### Imported job manually

All concreate classes of `JobInterface` in `job_a` and `job_b` will be automatically added into job registry
when they are imported in the script. _Jobs_ are executed in the order of importing modules.

**main.py**

```python
from manager import PipelineManager
from jobs import job_a, job_b

atomics = {'asset_data': ["/Game/A", "/Game/B"]}
manager = PipelineManager(atomics=atomics)
manager.add_registered_jobs()

parameters = (1, 2, "some_string", 1.234, ['element'], ('a', 'b'), {'k': 'v'})

manager.execute_jobs(*parameters)
```

_Atomics_ are shared variables in the pipeline, _jobs_ can access and modify them.

### Automated with pipeline config

Execute jobs with a config json file, which allows more flexible way to specify the module and exact `JobInterface`
classes. _Jobs_ are executed in the order as in the json file.

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
  ],
  "atomics": {
    "name": "Homer Simpson",
    "asset_data": [
      "/Game/A",
      "/Game/B"
    ]
  }
}
```

_Atomics_ can be defined in the config file and have **higher priority** than the same one in the `PipelineManager`
constructor, which means _Atomics_ in the config file can be extended in the initialization of `PipelineManager` but
they will not be overwritten by the code.

**main.py**

```python
from manager import PipelineManager
import pathlib

asset_data = ["/Game/C"]
atomics = {'asset_data': asset_data}

manager = PipelineManager(config_file=pathlib.Path(__file__).parent / "pipeline.json", atomics=atomics)
manager.add_registered_jobs()

parameters = (1, 2, "some_string", 1.234, ['element'], ('a', 'b'), {'k': 'v'})

manager.execute_jobs(*parameters)
```

---

Both of usage should give the same output as following:

```shell
$ python main.py
[JobA] atomics: {'asset_data': ['/Game/A', '/Game/B'], 'name': 'Homer Simpson'}, parameters: (1, 2, 'some_string', 1.234, ['element'], ('a', 'b'), {'k': 'v'})
[SomeNamedJob] atomics: {'asset_data': ['/Game/A', '/Game/B'], 'name': 'Homer Simpson'}, parameters: (1, 2, 'some_string', 1.234, ['element'], ('a', 'b'), {'k': 'v'})
```

## References

### Pipeline Manager

A `PipelineManager` starts a session of pipeline, and manage the lifecycle of it.

```python
from manager import PipelineManager
# you can manually import the Job Class
# from jobs import job_a

atomics = {"name": "Richard Feynman"} # extend the atomics in the config file

# config_file and atomics are optional for the PipelineManager,
# but it's suggested to use config to do the pipeline work.
manager = PipelineManager(config_file="/path/to/pipeline.json", atomics=atomics)

# this will add all jobs in job registry to the manager.
manager.add_registered_jobs()

parameters = (1, 2, "some_string", 1.234, ['element'], ('a', 'b'), {'k': 'v'})

# start the pipeline work
manager.execute_jobs(*parameters)
```

### Job

A Job is a concrete class of `JobInterface` and implements a `do()` method, the task of the job should be done in the
method.

```python
from interface import JobInterface


class JobA(JobInterface):
    def do(self, *parameters, atomics):
        print(f"[{self.__class__.__name__}] atomics: {atomics}, parameters: {parameters}")
        atomics['name'] = "Homer Simpson"
```

#### `do(self, *parameters, atomics)`

You will strictly implement the signature of this method in your Job Classes, **`atomics`** is a dict can be modified in
the job and is shared in the pipeline. **`parameters`** is dynamically set from `PipelineManager` when executing jobs.

### pipeline config

Config filename (`pipeline.json`) can be specified by user as long as properly used in the code.

| Key     | Type   | Description                                                                        |
|---------|--------|------------------------------------------------------------------------------------|
| jobs    | List   | Jobs to executed in the pipeline, specify the module and job class to be imported. |
| atomics | Object | Shared variables in the pipeline, can be modified by jobs.                         |

#### `jobs`

a list of jobs, used to locate the Job Class in the module. The jobs will be run in the order in the list. Note that the
manually imported Job Class in the code will also be counted in the pipeline queue.

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

#### `atomics`

An object (dict) that defines pipeline variables in the beginning. It can be used together with atomics defined in the
constructor of `PipelineManager`, but the atomics in the config file has the highest priority than others.

```json
{
  "atomics": {
    "name": "Homer Simpson",
    "asset_data": [
      "/Game/A",
      "/Game/B"
    ]
  }
}
```

```python
from manager import PipelineManager

atomics = {"asset_data": "/Game/C"}  # this won't work since we already have "asset_data" in the config file
manager = PipelineManager(config_file="/path/to/pipeline.json", atomics=atomics)
```

## Tests

```shell
python -m uniitest discover
```