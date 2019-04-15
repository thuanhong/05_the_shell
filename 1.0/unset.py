#!/usr/bin/env python3
from sys import argv


def unset_variable(arguments):
    for arg in arguments:
        if arg[0].isnumeric() or arg.startswith('='):
            print("intek-sh: unset: `" + arg + "': not a valid identifier")
        elif arg in environ:
            del environ[arg]


if __name__ == '__main__':
    unset_variable(argv[1:])
