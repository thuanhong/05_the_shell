#!/usr/bin/env python3
from os import environ
from input import read_input, handle_input
from logical import run_logical_operator


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

        run_logical_operator(user_input, set_vars)


if __name__ == '__main__':
    main()
