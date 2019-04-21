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


def glob_asterik(argument):
    """
    Solve test case: .*/.*/.* etc.

    Return a list of all possible path to glob
    """
    splitted_argument = argument.split("/")
    for index, key in enumerate(splitted_argument):
        if not key:
            splitted_argument.pop(index)
    number = len(splitted_argument)
    symbols = ['.', '..', '.*']
    # create all possible string from list of symbols, with 'number' of times
    keywords = ['/'.join(i) for i in product(symbols, repeat=number)]
    # if string has more than one asterik, remove that string
    for index, key in enumerate(keywords):
        if too_much_asterisk(key):
            keywords[index] = ""
    return keywords


def pre_globbing(arguments):
    """
    prepare for globbing

    Return a list of path
    """
    for index, argument in enumerate(arguments):
        if argument.startswith(".*"):
            arguments[index] = glob_asterik(argument)
        else:
            arguments[index] = [argument]
    return (" ".join(sum(arguments, []))).split()


def get_pathname_list(arguments):
    """
    Glob the path to find
    files and folders that user want to get

    Return a list of path after globbing
    """
    arguments = arguments.split()
    pathname_list = []
    for argument in pre_globbing(arguments):
        # check if program can glob the path or not
        # then add the globbed path to the list
        if glob(argument):
            pathname_list += sorted(glob(argument))
        elif not glob(argument) and ".*" not in argument:
            pathname_list += [argument]
    return (" ").join(pathname_list)
