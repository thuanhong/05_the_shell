from glob import glob
from itertools import product


def too_much_asterisk(key):
    count = 0
    for word in key:
        if word == "*":
            count += 1
    if count > 1:
        return True
    return False


def abc(arg):
    splitted_arg = arg.split("/")
    for index, key in enumerate(splitted_arg):
        if not key:
            splitted_arg.pop(index)

    number = len(splitted_arg)
    symbols = ['.', '..', '.*']
    keywords = ['/'.join(i) for i in product(symbols, repeat=number)]

    for index, key in enumerate(keywords):
        if too_much_asterisk(key):
            keywords[index] = ""

    return keywords


def pre_globbing(args):
    for index, arg in enumerate(args):
        if arg.startswith(".*"):
            args[index] = abc(arg)
        else:
            args[index] = [arg]

    return (" ".join(sum(args, []))).split()


def get_pathname_list(arguments):
    pathname_list = []
    for arg in pre_globbing(arguments):
        if glob(arg):
            pathname_list += sorted(glob(arg))
        elif not glob(arg) and ".*" not in arg:
            pathname_list += [arg]
    return pathname_list
