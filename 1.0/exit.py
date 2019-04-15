#!/usr/bin/env python3
from sys import argv


def exit_program(arguments):
    if not arguments:
        exit()
    else:
        pass


if __name__ == '__main__':
    exit_program(argv[1:])
