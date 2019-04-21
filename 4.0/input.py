from globbing import get_pathname_list
from tilde_expansion import expanse_tilde
from parameter_expansion import expanse_parameter, change_user_input
from command_substitution import command_sub
from handle_backslash import encode_backslash, decode_backslash, \
                             remove_backslash
from history import save_input, find_command_history
from logical_operator import split_logical_operator


def check_unfinished_input(string):
    """
    Check if user has finished input yet
    @param:  string: input from user
    @return: True if finished, False if not yet finished
    """
    if string.count('(') != string.count(')'):
        return True
    return False


def read_input():
    """
    Read input from user

    @return: string: input from user
    """
    string = input('\033[1;31mintek-sh$\033[00m ')
    while check_unfinished_input(string):
        string += input('\033[1;31m>\033[00m ')
    return string


def handle_input(user_input, set_vars, file_path, save_flag):
    """
    Handle input from user per specific case

    @param:  user_input: input from user
    @param:  set_vars: dictionary of variables
    @param:  file_path: history file path
    @param:  save_flag: boolean value check if need to save input or not

    @return: user_input: user input after handle
    """
    # find '!' command
    user_input = find_command_history(user_input, set_vars)
    # save input
    if save_flag:
        save_input(file_path, set_vars, user_input)
    # handle backslash 1
    user_input = encode_backslash(user_input)
    # handle tilde expansions
    user_input = expanse_tilde(user_input)
    # handle parameter expansions
    user_input = expanse_parameter(user_input)
    user_input = change_user_input(user_input)
    # handle globbing
    user_input = get_pathname_list(user_input)
    # handle command substitution with the backquotes
    user_input = command_sub(user_input)
    # handle backslash 2
    user_input = remove_backslash(user_input)
    user_input = decode_backslash(user_input)
    # handle logical operators
    user_input = split_logical_operator(user_input)
    return user_input
