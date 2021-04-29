import argparse
import sys
from pie import process_file, process_string


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse static files such as YAML and insert'
                                                 ' in them data from environment variables')
    parser.add_argument('-f', '--file', action='store', dest='file', help='Path to config file')
    parser.add_argument('-s', '--string', action='store', dest='string', help='String to precess')
    args = parser.parse_args()

    if not args.file and not args.string:
        raise ValueError('You should specify file or string')

    if args.file:
        process_file(args.file)
        sys.exit(0)

    if args.string:
        output = process_string(args.string)
        print(output)
        sys.exit(0)
