#!/usr/bin/env python3
from os import environ
from input import read_input, handle_input
from command import *


def setup_global_vars(environ_vars):
    var_list = {'exit_status': 0, 'history': []}
    var_list.update(environ_vars)
    return var_list


def main():
    set_vars = setup_global_vars(environ.copy())

    while True:
        user_input = read_input()
        print('--> raw input:', user_input)

        user_input = handle_input(user_input, set_vars)
        print('--> handle input:', user_input)

        if user_input:
            command, arguments = user_input[0], user_input[1:]
            if command == 'cd':
                change_current_dir(arguments, set_vars)
            elif command == 'printenv':
                print_env_variable(arguments)
            elif command == 'export':
                export_variable(arguments, set_vars)
            elif command == 'unset':
                unset_variable(arguments, set_vars)
            elif command == 'exit':
                exit_shell(arguments, set_vars)
            elif command == 'history':
                display_history(arguments, set_vars)
            elif user_input == ['echo', '$?']:
                print(set_vars['exit_status'])
            else:
                run_external_command(command, arguments, set_vars)


if __name__ == '__main__':
    main()
