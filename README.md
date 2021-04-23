# python-pie

[![Build Status](https://github.com/igorMIA/python-pie/actions/workflows/tests.yaml/badge.svg)](https://github.com/igorMIA/python-pie/actions/workflows/tests.yaml)
[![PyPI version](https://badge.fury.io/py/python-pie.svg)](https://badge.fury.io/py/python-pie)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-pie?style=plastic)

Python-pie(python insert env) reads key-value pairs from a `.env` file and can set them as environment
variables. It helps in the development of applications following the

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

```
hosts:
  - f"{host}"

loglevel: 4
f"{'log_file_path'}": f"/file/path/{filename or 'tmp.log'}"
log_rotate_count: 1
```

after `process_file(filepath)`

```
hosts:
  - localohst

loglevel: 4
log_file_path: /file/path/tmp.log
log_rotate_count: 1
```
