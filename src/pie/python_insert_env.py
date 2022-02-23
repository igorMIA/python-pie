import fileinput
import re
import os
import sys
from pathlib import Path
from shutil import copyfile

FSTRING_PATTERN = """f\"[^\"]+\""""
ENV_PATTERN = """({[^}{]+})+"""

BACKUP_EXTENSION = '.bak'


def process_string(string: str, env_file: str = None):
    """
    :param string: string to parse e.g.: 'log_file_path: f"/file/path/{log_file_path or 'tmp.log'}"'
    :param env_file: optional, path to environment file
    :return:
    """
    if env_file:
        _load_envs_from_file(env_file)

    def write_function(line, container):
        return line

    return _process([string], write_function)


def process_file(input_file: str, to_file: str = None, keep_input_file: bool = True, env_file: str = None):
    """
    :param input_file: path to file that should be processed
    :param to_file: optional, a path to file that should be created from input_file
    :param keep_input_file: keep original input file, in case to_file parameter provided
    :param env_file: optional, path to environment file
    :return:
    """
    if env_file:
        _load_envs_from_file(env_file)

    def write_function(line, container):
        sys.stdout.write(line)
        return container

    try:
        with fileinput.FileInput(input_file, inplace=True, backup=BACKUP_EXTENSION) as f:
            _process(f, write_function)

    # if catch exception, we want to restore original data from the backup file
    except Exception as e:
        file = Path(f.filename())
        try:
            file.unlink()
        except FileNotFoundError:
            pass
        os.rename(f'{file}{BACKUP_EXTENSION}', file)

        if isinstance(e, ValueError):
            raise
    finally:
        file = Path(f.filename())
        backup_file = Path(f'{file}{BACKUP_EXTENSION}')

        if to_file:
            if keep_input_file:
                copyfile(file, Path(file.parent, to_file))
                copyfile(backup_file, file)
            else:
                file.rename(Path(file.parent, to_file))

        try:
            backup_file.unlink()
        except FileNotFoundError:
            pass


def _process(strings_container, write):
    for line in strings_container:
        fstrings = re.findall(FSTRING_PATTERN, line)
        if fstrings:
            parsed_line = line
            for fstring in fstrings:
                pstrings = re.findall(ENV_PATTERN, fstring)
                fstring_buffer = fstring

                for pstring in pstrings:
                    parsed_pstring = pstring.replace('{', '').replace('}', '')
                    parsed_data = parsed_pstring.split(' or ')

                    if len(parsed_data) == 1:
                        env_data = os.getenv(parsed_data[0])
                        if env_data is None:
                            raise ValueError(f'env not found for {parsed_data}')
                        processed_data = env_data
                    elif len(parsed_data) == 2:
                        processed_data = os.getenv(parsed_data[0], parsed_data[1].replace("'", ''))
                    else:
                        raise ValueError(f'empty expression {pstring}')

                    fstring_buffer = re.sub(pstring, processed_data, fstring_buffer)

                parsed_line = re.sub(fstring, fstring_buffer[2:-1], parsed_line)
            strings_container = write(parsed_line, strings_container)
        else:
            strings_container = write(line, strings_container)
    return strings_container


def _load_envs_from_file(filename):
    with open(filename) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue

            key, value = line.strip().split('=', 1)
            os.environ[key] = value  # Load to local environ
