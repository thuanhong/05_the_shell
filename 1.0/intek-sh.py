#!/usr/bin/env python3
from os import environ
from subprocess import Popen
from input import read_input, handle_input


def control_loop():
    raw_input = read_input()
    user_input = handle_input(raw_input)
    if user_input:
        Popen(user_input).wait()


def main():
    while True:
        try:
            control_loop()
        except Exception as error_message:
            print('Crash: ', error_message)


def setup_builtins_env():
    import cd
    cd.environ = environ
    import printenv
    printenv.environ = environ
    import export
    export.environ = environ
    import unset
    unset.environ = environ


def setup_global_vars(environ_vars):
    var_list = {'exit_status': '0', 'history': []}
    var_list.update(environ_vars)
    return var_list


if __name__ == '__main__':
    global_vars = setup_global_vars(environ.copy())
    setup_builtins_env()
    main()
