from os import environ, listdir
from shutil import which
from readline import set_completer, parse_and_bind


def get_variables():

    list_variables = []
    for key in environ:
        list_variables.append(key)
    return list_variables


def find_executable_files(each_path, list_executable_files):
    try:
        for filename in listdir(each_path):
            if which(filename):
                list_executable_files.append(filename)
    except FileNotFoundError:
        pass

    return list_executable_files


def find_paths():
    list_paths = []
    list_executable_files = ['cd', 'exit', 'export', 'unset', 'history']
    try:
        for path in environ["PATH"].split(":"):
            path += "/"
            list_paths.append(path)
    except Exception:
        pass

    for each_path in list_paths:
        find_executable_files(each_path, list_executable_files)

    return list_executable_files


def get_completer_function(text, state):
    names = find_paths() + listdir('.') + get_variables()
    if not text or text == " ":
        names = listdir('.')
    options = [word for word in names if
               word.startswith(text.replace(" ", ""))]

    try:
        return options[state]
    except IndexError:
        return None


def auto_complete():
    set_completer(get_completer_function)
    parse_and_bind('tab: complete')
