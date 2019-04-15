#!/usr/bin/env python3
from subprocess import Popen
from input import read_input, handle_input


def control_loop():
    raw_input = read_input()
    cute_input = handle_input(raw_input)
    if cute_input:
        Popen(cute_input).wait()


def main():
    while True:
        control_loop()


if __name__ == '__main__':
    main()
