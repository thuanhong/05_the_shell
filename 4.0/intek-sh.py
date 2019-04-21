#!/usr/bin/env python3
from sys import argv
from os import environ
from os.path import dirname, abspath
from auto_completion import auto_complete
from input import read_input, handle_input
from logical_operator import run_logical_operator
from history import read_history_file
from signals_handling import control_signal


def create_variables(history_file_path):
    """
    Create a dictionary that store all shell's variables

    @param: path to the history file

    Return that dictionary
    """
    variables = {'exit_status': 0,
                 'history': read_history_file(history_file_path)}
    # add a copy of environ to the dictionary
    variables.update(environ.copy())
    return variables


def send_variables(set_variables):
    """
    Send local variable of this file to another files

    @param: dictionary of shell's variables
    """
    # Send shell's variables to file parameter_expansion
    import parameter_expansion as parameter_file
    parameter_file.set_variables = set_variables
    # Send shell's variables to file signals_handling
    import signals_handling as signal_file
    signal_file.set_variables = set_variables


def get_input_and_run(history_file_path, user_input, set_variables, flag):
    """
    Get input from user, turn it into runable command
    then run the command

    @param history_file_path: path to the history file
    @param user_input: user's input
    @param set_variables: shell variables
    @param flag: boolean, check if command is valid for saving to history
    """
    # get input
    if user_input:
        user_input = ' '.join(user_input)
    else:
        user_input = read_input()
    # turn raw input to readable command
    user_input = handle_input(user_input, set_variables,
                              history_file_path, flag)
    # run command
    run_logical_operator(user_input, set_variables)


def main():
    """
    Control the main flow of the program
    Catch exceptions if any occur
    """
    # search file history's path
    history_file_path = dirname(abspath(__file__)) + '/.history.txt'
    # create a dictionary of shell's variables
    set_variables = create_variables(history_file_path)
    # send shell's variables to another files
    send_variables(set_variables)
    # handle user's signal
    control_signal()
    # handle auto completion when press TAB
    auto_complete()
    user_input = argv[1:]
    # if this file is called with arguments, read and run that arguments
    if user_input:
        get_input_and_run(history_file_path, user_input, set_variables, False)
    else:
        # if no arguments, demand user to give input
        while True:
            try:
                get_input_and_run(history_file_path, user_input,
                                  set_variables, True)
            # handle Crtl C
            except KeyboardInterrupt:
                print('^C')
            # handle Crtl D
            except EOFError:
                print()
                quit()


if __name__ == '__main__':
    main()
