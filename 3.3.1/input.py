from completion import auto_complete
from globbing import get_pathname_list
from tilde_expansion import tilde
from param_expansion import param, change_user_input
from command_sub import command_sub
from handle_backslash import encode_backslash, decode_backslash, remove_backslash
from history import save_input, find_command_history
from logical import split_logical_operator


def check_unfinished_input(string):
    return False


def read_input():
    auto_complete()
    string = input('\033[1;31mintek-sh$\033[00m ')
    while check_unfinished_input(string):
        string += input('\033[1;31m>\033[00m ')
    return string


def handle_input(user_input, set_vars, file_path):

    user_input = user_input.replace("$?", str(set_vars["exit_status"]))
    user_input = change_user_input(user_input)
    print('filter -1:', user_input)

    # find '!':
    user_input = find_command_history(user_input, set_vars)
    print('filter 0:', user_input)

    # save:
    save_input(file_path, set_vars, user_input)

    # backslash:
    user_input = encode_backslash(user_input)
    print('filter 1:', user_input)

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

    user_input = remove_backslash(user_input)
    user_input = decode_backslash(user_input)
    print('filter 6:', user_input)

    # $?:
    user_input = user_input.replace('$?', str(set_vars['exit_status']))
    print('filter 7:', user_input)

    # logical:
    user_input = split_logical_operator(user_input)
    print('filter 8:', user_input)

    return user_input
