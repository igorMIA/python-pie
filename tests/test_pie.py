import os
import pytest
from src.pie import process_file, process_string


TEST_CASE_1_2_INPUT = """
hosts:
  - "localhost"

loglevel: 4
log_file_path: f"/file/path/{log_file_path or 'tmp.log'}"
log_rotate_count: 1
"""


TEST_CASE_3_INPUT = """
hosts:
  - f"{aboba}"

loglevel: 4
log_file_path: f"/file/path/{log_file_path or 'tmp.log'}"
log_rotate_count: 1
"""


TEST_CASE_4_INPUT = """
hosts:
  - "localhost"

loglevel: 4
f"{parameter or 'log_file_path'}": f"/file/path/{log_file_path or 'tmp.log'}"
log_rotate_count: 1
"""


TEST_CASE_5_INPUT = """
hosts:
  - "f"{host}""

loglevel: 4
f"{parameter or 'log_file_path'}": f"/file/path/{log_file_path or 'tmp.log'}"
log_rotate_count: 1
"""


TEST_CASE_6_INPUT = """
hosts:
  - "localhost"

loglevel: 4
log_file_path: f"/file/path/{log_file_path or 'tmp.log'}}}}}"
log_rotate_count: 1
"""


TEST_CASE_7_INPUT = """
hosts:
  - "localhost"

loglevel: 4
log_file_path: fffff"/file/path/{log_file_path or 'tmp.log'}"
log_rotate_count: 1
"""


TEST_CASE_1_4_5_OUTPUT = """
hosts:
  - "localhost"

loglevel: 4
log_file_path: /file/path/tmp.log
log_rotate_count: 1
"""


TEST_CASE_2_OUTPUT = """
hosts:
  - "localhost"

loglevel: 4
log_file_path: /file/path/env_file.tmp
log_rotate_count: 1
"""


TEST_CASE_6_OUTPUT = """
hosts:
  - "localhost"

loglevel: 4
log_file_path: /file/path/tmp.log}}}}
log_rotate_count: 1
"""


TEST_CASE_7_OUTPUT = """
hosts:
  - "localhost"

loglevel: 4
log_file_path: ffff/file/path/tmp.log
log_rotate_count: 1
"""


def test_process_file_without_env(tmpdir):
    input_file = tmpdir.mkdir('tmp').join('input.txt')
    input_file.write(TEST_CASE_1_2_INPUT)

    process_file(input_file)

    content = input_file.read()
    input_file.remove()

    assert content == TEST_CASE_1_4_5_OUTPUT


def test_process_file_with_env(tmpdir):
    input_file = tmpdir.mkdir('tmp').join('input.txt')
    input_file.write(TEST_CASE_1_2_INPUT)

    os.environ['log_file_path'] = 'env_file.tmp'

    process_file(input_file)

    content = input_file.read()
    del os.environ['log_file_path']
    input_file.remove()

    assert content == TEST_CASE_2_OUTPUT


def test_process_file_without_env_should_raise_error(tmpdir):
    input_file = tmpdir.mkdir('tmp').join('input.txt')
    input_file.write(TEST_CASE_3_INPUT)

    with pytest.raises(ValueError):
        process_file(input_file)

    input_file.remove()


def test_process_file_with_multiple_fstrings(tmpdir):
    input_file = tmpdir.mkdir('tmp').join('input.txt')
    input_file.write(TEST_CASE_4_INPUT)

    process_file(input_file)

    content = input_file.read()
    input_file.remove()

    assert content == TEST_CASE_1_4_5_OUTPUT


def test_process_file_with_multiple_fstrings_on_different_strings(tmpdir):
    input_file = tmpdir.mkdir('tmp').join('input.txt')
    input_file.write(TEST_CASE_5_INPUT)

    os.environ['host'] = 'localhost'

    process_file(input_file)

    content = input_file.read()
    del os.environ['host']
    input_file.remove()

    assert content == TEST_CASE_1_4_5_OUTPUT


def test_process_file_with_incorrect_fstring_syntax_1(tmpdir):
    input_file = tmpdir.mkdir('tmp').join('input.txt')
    input_file.write(TEST_CASE_6_INPUT)

    process_file(input_file)

    content = input_file.read()
    input_file.remove()

    assert content == TEST_CASE_6_OUTPUT


def test_process_file_with_incorrect_fstring_syntax_2(tmpdir):
    input_file = tmpdir.mkdir('tmp').join('input.txt')
    input_file.write(TEST_CASE_7_INPUT)

    process_file(input_file)

    content = input_file.read()
    input_file.remove()

    assert content == TEST_CASE_7_OUTPUT


def test_process_string():
    output = process_string(TEST_CASE_1_2_INPUT)

    assert output == TEST_CASE_1_4_5_OUTPUT
