import argparse
import fileinput
import re
import os
import sys


FSTRING_PATTERN = """f\"[^\"]+\""""
ENV_PATTERN = """({[^}{]+})+"""

BACKUP_EXTENSION = '.bak'


def process_string(string):
    """

    :return:
    """

    def write_function(line, container):
        return line

    return _process([string], write_function)


def process_file(file):
    """
    E.g:
    logging:
        log_file_path: f"/file/path/{log_file_path or 'tmp.log'}"

    logging:
        log_file_path: /file/path/x54.log.txt

    :param file:
    :return:
    """
    def write_function(line, container):
        sys.stdout.write(line)
        return container

    try:
        with fileinput.FileInput(file, inplace=True, backup=BACKUP_EXTENSION) as file:
            _process(file, write_function)
    except Exception as e:
        if isinstance(file, fileinput.FileInput):
            file = file.filename()
        os.remove(file)
        os.rename(f'{file}.bak', file)

        if isinstance(e, ValueError):
            raise


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse static files such as YAML and insert'
                                                 ' in them data from environment variables')
    parser.add_argument('-f', '--file', action='store', dest='file', help='Path to config file')
    parser.add_argument('-s', '--string', action='store', dest='string', help='Path to config file')
    args = parser.parse_args()

    if not args.file and not args.string:
        raise ValueError('You should specify file or string')

    if args.file:
        process_file(args.file)
        try:
            os.remove(f'{args.file}{BACKUP_EXTENSION}')
        except OSError:
            pass
        sys.exit(0)

    if args.string:
        output = process_string(args.string)
        print(output)
        sys.exit(0)
