#!/usr/bin/env python3
from subprocess import Popen
from input import read_input, handle_input
from command import *


def control_loop():
    raw_input = read_input()
    cute_input = handle_input(raw_input)
    if cute_input:
        command, arguments = cute_input[0], cute_input[1:]
        if command == 'cd':
            change_current_dir(arguments)
        elif command == 'printenv':
            print_env_variable(arguments)
        elif command == 'export':
            export_variable(arguments)
        elif command == 'unset':
            unset_variable(arguments)
        elif command == 'exit':
            exit_shell(arguments)
        elif command == 'history':
            display_history(arguments)
        else:
            run_external_command(command, arguments)


def main():
    while True:
        control_loop()


if __name__ == '__main__':
    main()
