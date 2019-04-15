from completion import auto_complete


def check_unfinished_input(string):
    return False


def read_input():
    auto_complete()
    string = input('\033[1;31mintek-sh$\033[00m ')
    while check_unfinished_input(string):
        string += input('\033[1;31m>\033[00m ')
    return string
