from os import environ
from completion import auto_complete
from globbing import get_pathname_list
from tilde_expansion import tilde
from param_expansion import param
from command_sub import command_sub
from handle_backslash import handle_backslash


def check_unfinished_input(string):
    return False


def read_input():
    auto_complete()
    string = input('\033[1;31mintek-sh$\033[00m ')
    while check_unfinished_input(string):
        string += input('\033[1;31m>\033[00m ')
    return string


def handle_input(user_input):
    #encode_backslash(user_input)
    # tilde:
    user_input = tilde(user_input)
    print('filter 2:', user_input)

    # param:
    user_input = param(user_input)
    print('filter 3:', user_input)

    # globbing:
    user_input = get_pathname_list(user_input)
    print('filter 4:', user_input)

    # command sub:
    user_input = command_sub(user_input)
    print('filter 5:', user_input)
    return user_input.split()
