# Pypline 🐍 📦

Create your custom Pipeline in Python script.

A **Pipeline** consists of the different jobs and executes them in the order. A **Job** is an action node (python
function) in the pipeline, jobs share pipeline variables called **Atomics** which can be modified by jobs.

## How to use

### Importing job manually

All concrete classes of `JobInterface` in `job_a` and `job_b` will be automatically added into Job Registry
when they are imported in the script. _Jobs_ are executed in the order of importing modules.

**main.py**

```python
from pypline import Pipeline
# jobs will be added to job registry when importing their modules
from jobs import job_a, job_b

atomics = {'asset_data': ["/Game/A", "/Game/B"]}
manager = Pipeline(atomics=atomics)

# this will add jobs in job registry to the pipeline manager
manager.add_registered_jobs()

parameters = (1, 2, "some_string", 1.234, ['element'], ('a', 'b'), {'k': 'v'})

# start the jobs in the order of imports
manager.execute_jobs(*parameters)
```

_Atomics_ are shared variables in the pipeline, _jobs_ can access and modify them.

### Automation with pipeline config

Execute jobs with a config json file, which allows a more flexible way to specify the module and exact `JobInterface`
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
      "class": "JobB"
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

_Atomics_ can be defined in the config file and have **higher priority** than the same one in the `Pipeline`
constructor, which means _Atomics_ in the config file can be extended in the initialization of `Pipeline` but
they will not be overwritten by the code.

**main.py**

```python
from pypline import Pipeline
import pathlib

asset_data = ["/Game/C"]
atomics = {'asset_data': asset_data}

manager = Pipeline(config_file=pathlib.Path(__file__).parent / "pipeline.json", atomics=atomics)
manager.add_registered_jobs()

parameters = (1, 2, "some_string", 1.234, ['element'], ('a', 'b'), {'k': 'v'})

manager.execute_jobs(*parameters)
```

---

Both usages should give the same output as follows:

```shell
$ python example.py
[JobA] atomics: {'asset_data': ['/Game/A', '/Game/B'], 'name': 'Homer Simpson'}, parameters: (1, 2, 'some_string', 1.234, ['element'], ('a', 'b'), {'k': 'v'})
[JobB] atomics: {'asset_data': ['/Game/A', '/Game/B'], 'name': 'Homer Simpson'}, parameters: (1, 2, 'some_string', 1.234, ['element'], ('a', 'b'), {'k': 'v'})
```

## References
> [!WARNING]  
> We are at the early stage of development, APIs are subject to change.

### Pipeline (Pipeline Manager)

A `Pipeline` starts a session of pipeline, and manages the lifecycle of it.

```python
from pypline import Pipeline

# you can manually import the Job Class
# from jobs import job_a

atomics = {"name": "Richard Feynman"}  # extend the atomics in the config file

# config_file and atomics are optional for the Pipeline,
# but it's suggested to use config to do the pipeline work.
manager = Pipeline(config_file="/path/to/pipeline.json", atomics=atomics)

# this will add all jobs in job registry to the manager.
manager.add_registered_jobs()

parameters = (1, 2, "some_string", 1.234, ['element'], ('a', 'b'), {'k': 'v'})

# start the pipeline work
manager.execute_jobs(*parameters)
```

### Job

A Job is a concrete class of `JobInterface` and implements a `do()` method, the task of the job should be done in the
method.

When the Job module is imported into the script, the Job Class will be automatically added to Job Registry.

```python
from interface import JobInterface


class JobA(JobInterface):
    def do(self, *parameters, atomics):
        print(f"[{self.__class__.__name__}] atomics: {atomics}, parameters: {parameters}")
        atomics['name'] = "Homer Simpson"
```

#### `do(self, *parameters, atomics)`

You will strictly implement the signature of this method in your Job Classes, **`atomics`** is a dict that can be modified in
the job and is shared in the pipeline. **`parameters`** is dynamically set from `Pipeline` when executing jobs.

##### parameters

> [!NOTE]
> TODO: each `parameters` is expected to be made for each Job, but we currently use global `parameters` for all jobs.

### Pipeline config

Config filename (`pipeline.json`) can be specified by the user as long as properly used in the code.

| Key     | Type   | Description                                                                        |
|---------|--------|------------------------------------------------------------------------------------|
| jobs    | List   | Jobs to be executed in the pipeline, specify the module and job class to be imported. |
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
      "class": "JobB"
    }
  ]
}
```

#### `atomics`

An object (dict) that defines pipeline variables in the beginning. It can be used together with atomics defined in the
constructor of `Pipeline`, but the atomics in the config file has the highest priority over others.

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
from pypline import Pipeline

atomics = {"asset_data": "/Game/C"}  # this won't work since we already have "asset_data" in the config file
manager = Pipeline(config_file="/path/to/pipeline.json", atomics=atomics)
```

## Tests

```shell
python -m uniitest discover
```
