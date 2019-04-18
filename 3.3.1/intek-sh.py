#!/usr/bin/env python3
from os import environ
from input import read_input, handle_input
from logical import run_logical_operator
from argparse import ArgumentParser
from sys import argv
from os.path import dirname, abspath
from history import read_history_file
import param_expansion as file



def create_variables():
    variables = {'exit_status': 0, 'history': read_history_file(dirname(abspath(__file__)) + '/.history.txt')}
    variables.update(environ.copy())
    return variables


def main():
    user_input = argv[1:]
    variables = create_variables()
    file.set_variables = variables
    if not user_input:
        while True:
            user_input = read_input()
            print('--> raw input:', user_input)

            user_input = handle_input(user_input, variables)
            print('--> handle input:', user_input)

            run_logical_operator(user_input, variables)
    else:
        user_input = ' '.join(user_input)
        print('--> raw input:', user_input)
        user_input = handle_input(user_input, variables)
        print('--> handle input:', user_input)

        run_logical_operator(user_input, variables)


if __name__ == '__main__':
    main()
