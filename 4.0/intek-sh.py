#!/usr/bin/env python3
from sys import argv
from os import environ
from os.path import dirname, abspath
from auto_completion import auto_complete
from input import read_input, handle_input
from logical import run_logical_operator
from history import read_history_file
from signals_handling import control_signal


def create_variables(history_file_path):
    variables = {'exit_status': 0,
                 'history': read_history_file(history_file_path)}
    variables.update(environ.copy())
    return variables


def send_variables(set_variables):
    import parameter_expansion as param_file
    param_file.set_variables = set_variables
    import signals_handling as signal_file
    signal_file.set_variables = set_variables


def control(history_file_path, user_input, set_variables, flag):
    if user_input:
        user_input = ' '.join(user_input)
    else:
        user_input = read_input()
    user_input = handle_input(user_input, set_variables, history_file_path, flag)
    run_logical_operator(user_input, set_variables)


def main():
    history_file_path = dirname(abspath(__file__)) + '/.history.txt'
    set_variables = create_variables(history_file_path)
    send_variables(set_variables)
    control_signal()
    auto_complete()
    user_input = argv[1:]
    if user_input:
        control(history_file_path, user_input, set_variables, False)
    else:
        while True:
            try:
                control(history_file_path, user_input, set_variables, True)
            except KeyboardInterrupt:
                print('^C')
            except EOFError:
                print()
                quit()


if __name__ == '__main__':
    main()
