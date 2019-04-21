from os import environ, listdir
from shutil import which
from readline import set_completer, parse_and_bind


def get_variables():
    """
    Get all shell's variables

    Return a list of shell's variables
    """
    list_variables = []
    for key in environ:
        list_variables.append(key)
    return list_variables


def find_executable_files(each_path, list_executable_files):
    """
    Search for executable files inside a given path

    Return list of files name
    """
    try:
        for filename in listdir(each_path):
            # if filename is executable file inside $PATH
            if which(filename):
                list_executable_files.append(filename)
    except FileNotFoundError:
        pass
    return list_executable_files


def find_paths():
    """
    Search for executable files inside $PATH

    Return list of files name
    """
    list_paths = []
    list_executable_files = ['cd', 'exit', 'export', 'unset', 'history']
    try:
        # create a list of path from $PATH
        for path in environ["PATH"].split(":"):
            path += "/"
            list_paths.append(path)
    except Exception:
        pass
    # search for files inside each path
    for each_path in list_paths:
        find_executable_files(each_path, list_executable_files)
    return list_executable_files


def get_completer_function(text, state):
    """
    Search for invalid options

    @param text: user's unfinished input

    Return the corresponding option
    """
    # default list of options
    names = find_paths() + listdir('.') + get_variables()
    # only current files and folder listed
    if not text or text == " ":
        names = listdir('.')
    # search for valid options
    options = [word for word in names if
               word.startswith(text.replace(" ", ""))]
    try:
        return options[state]
    except IndexError:
        return None


def auto_complete():
    """
    Auto complete the string while pressing tab
    """
    set_completer(get_completer_function)
    parse_and_bind('tab: complete')
