#!/usr/bin/env python3
from sys import argv


def export_variable(arguments):
    if arguments:
        for arg in arguments:
            if arg[0].isnumeric() or arg.startswith('='):
                print("intek-sh: export: `" + arg +
                      "': not a valid identifier")
            elif '=' in arg:
                pos = arg.find('=')
                environ[arg[:pos]] = arg[pos + 1:]
    else:
        for key, value in sorted(environ.items()):
            print('export ' + key + '=' + value)


if __name__ == '__main__':
    export_variable(argv[1:])
