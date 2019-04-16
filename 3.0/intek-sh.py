#!/usr/bin/env python3
from input import read_input, handle_input
from command import *


def main():
    while True:
        user_input = read_input()
        print('--> raw input:', user_input)

        user_input = handle_input(user_input)
        print('--> handle input:', user_input)

        if user_input:
            command, arguments = user_input[0], user_input[1:]
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


if __name__ == '__main__':
    main()
