from os import environ
from completion import auto_complete
from globbing import get_pathname_list
from tilde_expansion import tilde
from param_expansion import param
from command_sub import command_sub


def check_unfinished_input(string):
    return False


def read_input():
    auto_complete()
    string = input('\033[1;31mintek-sh$\033[00m ')
    while check_unfinished_input(string):
        string += input('\033[1;31m>\033[00m ')
    return string


def handle_input(raw_input):
    # split (' '):
    user_input = raw_input.split()
    print('filter 1:', user_input)

    # tilde:
    if len(user_input) > 1:
        user_input = user_input[:1] + tilde(user_input[1:])
    print('filter 2:', user_input)

    # param:
    if len(user_input) > 1:
        user_input = user_input[:1] + param(user_input[1:])
    print('filter 3:', user_input)

    # globbing:
    if len(user_input) > 1:
        user_input = user_input[:1] + get_pathname_list(user_input[1:])
    print('filter 4:', user_input)

    # command sub:
    user_input = command_sub([' '.join(user_input)])
    print('filter 5:', user_input)

    return user_input.split()
