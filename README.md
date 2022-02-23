# python-pie

[![Build Status](https://github.com/igorMIA/python-pie/actions/workflows/tests.yaml/badge.svg)](https://github.com/igorMIA/python-pie/actions/workflows/tests.yaml)
[![PyPI version](https://badge.fury.io/py/python-pie.svg)](https://badge.fury.io/py/python-pie)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-pie?style=plastic)

Python-pie(python insert env) parses static files such as YAML and insert in them data from environment variables

- [Getting Started](#getting-started)
- [Syntax example](#syntax-example)
- [Using as module from command line](#using-as-module-from-command-line)
- [Docker example](#docker-example)
- [Run tests](#run-tests)

## Getting Started

```shell
pip install python-pie
```

You can use python-pie to insert env variables to static configurations,
like that:

```python
from pie import process_file

filepath = '/docker/configuration.yaml'
process_file(filepath)
```

The syntax of files supported by python-pie is similar
to that of python [fstrings](https://www.python.org/dev/peps/pep-0498/):

`f"54 {from_env or 'default_value'} some text"`

Depends if your environment has a from_env variable or not, python-pie will load it,
or in case of absence take the default value


### Syntax example

```yaml
hosts:
  - f"{host}"

loglevel: 4
f"{'log_file_path'}": f"/file/path/{filename or 'tmp.log'}"
log_rotate_count: 1
```

after `process_file(filepath)`

```yaml
hosts:
  - localohst

loglevel: 4
log_file_path: /file/path/tmp.log
log_rotate_count: 1
```

### Using as module from command line

You can use python-pie in command line.
```shell
python -m pie -f /node54/config.yml
```

Flags:
*(you should provide at least one of those)*

- `-f --file` path to config file.
- `-s --string` string to precess.

*optional*:
- `-tf --to-file` path to output config file.
- `--keep-file` if pie should keep original file without change.

### Docker example

```shell
docker create -t --name pie -i python:3.9 || true;
docker start pie;
docker exec pie python -m pip install python-pie;
docker exec pie python -m pie -f /node54/config.yml;
```

during build:

```shell
FROM python:3.9-alpine AS builder
RUN pip install python-pie
RUN python -m pie -f /tmp/template.yml -tf /app/config.yml -e .env
```

### Run tests

To run tests install `pytest` library and run the command: 

```shell
pytest tests/
```
