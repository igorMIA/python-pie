import os
import pytest
from src.pie import process_file, process_string


INPUT_FILE_NAME = 'input.txt'
OUTPUT_FILE_NAME = 'output.txt'


TEST_CASE_1_2_9_11_12_INPUT = """
hosts:
  - "localhost"

loglevel: 4
log_file_path: f"/file/path/{log_file_path or 'tmp.log'}"
log_rotate_count: 1
"""


TEST_CASE_3_10_INPUT = """
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

TEST_CASE_8_INPUT = 'log_file_path: f"/file/path/{log_file_path or \'tmp.log\'}"'


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


TEST_CASE_8_OUTPUT = 'log_file_path: /file/path/tmp.log'


def test_process_file_without_env(tmpdir):
    input_file = tmpdir.mkdir('tmp').join(INPUT_FILE_NAME)
    input_file.write(TEST_CASE_1_2_9_11_12_INPUT)

    process_file(input_file)

    content = input_file.read()
    input_file.remove()

    assert content == TEST_CASE_1_4_5_OUTPUT


def test_process_file_with_env(tmpdir):
    input_file = tmpdir.mkdir('tmp').join(INPUT_FILE_NAME)
    input_file.write(TEST_CASE_1_2_9_11_12_INPUT)

    os.environ['log_file_path'] = 'env_file.tmp'

    process_file(input_file)

    content = input_file.read()
    del os.environ['log_file_path']
    input_file.remove()

    assert content == TEST_CASE_2_OUTPUT


def test_process_file_without_env_should_raise_error(tmpdir):
    input_file = tmpdir.mkdir('tmp').join(INPUT_FILE_NAME)
    input_file.write(TEST_CASE_3_10_INPUT)

    with pytest.raises(ValueError):
        process_file(input_file)

    input_file.remove()


def test_process_file_with_multiple_fstrings(tmpdir):
    input_file = tmpdir.mkdir('tmp').join(INPUT_FILE_NAME)
    input_file.write(TEST_CASE_4_INPUT)

    process_file(input_file)

    content = input_file.read()
    input_file.remove()

    assert content == TEST_CASE_1_4_5_OUTPUT


def test_process_file_with_multiple_fstrings_on_different_strings(tmpdir):
    input_file = tmpdir.mkdir('tmp').join(INPUT_FILE_NAME)
    input_file.write(TEST_CASE_5_INPUT)

    os.environ['host'] = 'localhost'

    process_file(input_file)

    content = input_file.read()
    del os.environ['host']
    input_file.remove()

    assert content == TEST_CASE_1_4_5_OUTPUT


def test_process_file_with_incorrect_fstring_syntax_1(tmpdir):
    input_file = tmpdir.mkdir('tmp').join(INPUT_FILE_NAME)
    input_file.write(TEST_CASE_6_INPUT)

    process_file(input_file)

    content = input_file.read()
    input_file.remove()

    assert content == TEST_CASE_6_OUTPUT


def test_process_file_with_incorrect_fstring_syntax_2(tmpdir):
    input_file = tmpdir.mkdir('tmp').join(INPUT_FILE_NAME)
    input_file.write(TEST_CASE_7_INPUT)

    process_file(input_file)

    content = input_file.read()
    input_file.remove()

    assert content == TEST_CASE_7_OUTPUT


def test_process_string():
    output = process_string(TEST_CASE_8_INPUT)

    assert output == TEST_CASE_8_OUTPUT


def test_process_file_backup_file_deletion(tmpdir):
    input_file = tmpdir.mkdir('tmp').join(INPUT_FILE_NAME)
    input_file.write(TEST_CASE_1_2_9_11_12_INPUT)

    process_file(input_file)

    assert os.listdir(input_file.dirname) == [INPUT_FILE_NAME]
    input_file.remove()


def test_process_file_backup_if_exception_raised(tmpdir):
    input_file = tmpdir.mkdir('tmp').join(INPUT_FILE_NAME)
    input_file.write(TEST_CASE_3_10_INPUT)

    with pytest.raises(ValueError):
        process_file(input_file)

    content = input_file.read()
    input_file.remove()

    assert content == TEST_CASE_3_10_INPUT


def test_process_file_with_rename_should_not_remove_original_file(tmpdir):
    input_file = tmpdir.mkdir('tmp').join(INPUT_FILE_NAME)
    input_file.write(TEST_CASE_1_2_9_11_12_INPUT)

    process_file(input_file, OUTPUT_FILE_NAME)

    assert os.listdir(input_file.dirname) == [INPUT_FILE_NAME, OUTPUT_FILE_NAME]


def test_process_file_with_rename_should_remove_original_file(tmpdir):
    input_file = tmpdir.mkdir('tmp').join(INPUT_FILE_NAME)
    input_file.write(TEST_CASE_1_2_9_11_12_INPUT)

    process_file(input_file, OUTPUT_FILE_NAME, keep_input_file=False)

    assert os.listdir(input_file.dirname) == [OUTPUT_FILE_NAME]
