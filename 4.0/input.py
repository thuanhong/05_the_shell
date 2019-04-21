from globbing import get_pathname_list
from tilde_expansion import expanse_tilde
from param_expansion import expanse_parameter, change_user_input
from command_sub import command_sub
from handle_backslash import encode_backslash, decode_backslash, remove_backslash
from history import save_input, find_command_history
from logical import split_logical_operator


def check_unfinished_input(string):
    if string.count('(') != string.count(')'):
        return True
    return False


def read_input():
    string = input('\033[1;31mintek-sh$\033[00m ')
    while check_unfinished_input(string):
        string += input('\033[1;31m>\033[00m ')
    return string


def handle_input(user_input, set_vars, file_path, save_flag):

    # find '!':
    user_input = find_command_history(user_input, set_vars)

    # save:
    if save_flag:
        save_input(file_path, set_vars, user_input)

    # backslash:
    user_input = encode_backslash(user_input)

    # tilde:
    user_input = expanse_tilde(user_input)

    # param:
    user_input = expanse_parameter(user_input)
    user_input = change_user_input(user_input)

    # globbing:
    user_input = get_pathname_list(user_input)

    # command sub:
    user_input = command_sub(user_input)

    user_input = remove_backslash(user_input)
    user_input = decode_backslash(user_input)

    # logical:
    user_input = split_logical_operator(user_input)

    return user_input
