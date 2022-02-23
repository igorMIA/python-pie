import argparse
import sys
from pie import process_file, process_string


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse static files such as YAML and insert'
                                                 ' in them data from environment variables')
    parser.add_argument('-f', '--file', action='store', dest='file', help='Path to config file')
    parser.add_argument('-tf', '--to-file', action='store', dest='output_file', help='Path to output config file')
    parser.add_argument('--keep-file', action='store_false', dest='keep_file',
                        help='If pie should keep original file without change')
    parser.add_argument('-s', '--string', action='store', dest='string', help='String to precess')
    parser.add_argument('-e', '--env-file', action='store', dest='env_file', help='Path to env file')
    parser.set_defaults(keep_file=True)
    args = parser.parse_args()

    if not args.file and not args.string:
        raise ValueError('You should specify file or string')

    if args.file:
        process_file(args.file, args.output_file, args.keep_file, args.env_file)
        sys.exit(0)

    if args.string:
        output = process_string(args.string, args.env_file)
        print(output)
        sys.exit(0)
