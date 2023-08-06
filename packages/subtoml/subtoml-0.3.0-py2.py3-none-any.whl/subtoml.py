#!/usr/bin/env python
from __future__ import print_function

import optparse
import sys

from pytoml import dump, load

__all__ = 'main',
__version__ = '0.3.0'


parser = optparse.OptionParser(version='%prog ' + __version__)
parser.add_option('-i', '--input-file', metavar='FILE', default='-',
                  help='TOML file to read. [%default]')
parser.add_option('-o', '--output-file', metavar='FILE', default='-',
                  help='TOML file to write. [%default]')
parser.add_option('-d', '--delete', '--delete-key',
                  dest='delete_keys', metavar='KEY',
                  action='append', default=[],
                  help='Remove the key.  This option can be repeated.')


def find_container(container, key):
    keys = key.split('.')
    key_path = ''
    for k in keys[:-1]:
        key_path += (k and '.') + k
        try:
            container = container[k]
        except KeyError:
            return parser.error('failed to find ' + key_path)
    return container, keys[-1]


def main():
    options, args = parser.parse_args()
    if len(args) % 2 == 1:
        return parser.error('keys and values must be paired')
    elif not (args or options.delete_keys):
        return parser.error('key/value pairs are missing')
    pairs = zip(args[::2], args[1::2])
    if options.input_file == '-':
        try:
            table = load(sys.stdin)
        except KeyboardInterrupt:
            raise SystemExit(130)
    else:
        with open(options.input_file) as f:
            table = load(f)
    for k in options.delete_keys:
        try:
            container, leaf_key = find_container(table, k)
            del container[leaf_key]
        except KeyError:
            pass
    for k, v in pairs:
        container, leaf_key = find_container(table, k)
        try:
            container[leaf_key] = v
        except KeyError:
            return parser.error('failed to find ' + k)
    if options.output_file == '-':
        dump(table, sys.stdout, sort_keys=True)
    else:
        with open(options.output_file, 'w') as f:
            dump(table, f, sort_keys=True)
    raise SystemExit(0)


if __name__ == '__main__':
    main()
