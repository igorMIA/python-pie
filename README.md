# python-pie

[![PyPI version](https://badge.fury.io/py/python-pie.svg)](https://badge.fury.io/py/python-pie)

Python-pie reads key-value pairs from a `.env` file and can set them as environment
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
