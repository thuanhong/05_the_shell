#!/usr/bin/env python3
from sys import argv


def print_env_variable(arguments):
    if arguments:
        for arg in arguments:
            if arg in environ:
                print(environ[arg])
    else:
        for key, value in environ.items():
            print(key + '=' + value)


if __name__ == '__main__':
    print_env_variable(argv[1:])
