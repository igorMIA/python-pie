import os

import pytest


INPUT_FILE_NAME = 'input.txt'
OUTPUT_FILE_NAME = 'output.txt'
ENV_FILE_NAME = '.env'


ENV_FILE_CONTENT = """
count=10
host=localhost
#var=something

"""


@pytest.fixture
def input_file(tmpdir):
    input_file = tmpdir.mkdir('tmp').join(INPUT_FILE_NAME)
    yield input_file
    try:
        input_file.remove()
    except OSError:
        pass


@pytest.fixture
def env_file(tmpdir):
    file = tmpdir.mkdir('env').join(ENV_FILE_NAME)
    file.write(ENV_FILE_CONTENT)
    yield file
    file.remove()
    del os.environ['count']
    del os.environ['host']
