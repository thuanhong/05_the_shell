from os.path import expanduser, exists, isdir
from os import environ


def get_user_directory(username):
    user_directory = expanduser("~") + "/../" + username.split("/")[0][1:]

    if exists(user_directory) and isdir(user_directory):
        return expanduser("~") + "/../" + username[1:]

    return username


def tilde_expansion(raw_arguments,
                    pwd_exist, oldpwd_exist,
                    current_dir, previous_dir):

    for index, argument in enumerate(raw_arguments):
        if argument == "~" or argument.startswith("~/"):
            raw_arguments[index] = expanduser(argument)

        elif pwd_exist and argument == "~+":
            raw_arguments[index] = current_dir
        elif pwd_exist and argument.startswith("~+"):
            raw_arguments[index] = current_dir + argument[2:]

        elif oldpwd_exist and argument == "~-":
            raw_arguments[index] = previous_dir
        elif oldpwd_exist and argument.startswith("~-"):
            raw_arguments[index] = previous_dir + argument[2:]

        elif argument.startswith("~") and not argument.startswith("~-") and not argument.startswith("~+"):
            raw_arguments[index] = get_user_directory(argument)

    return raw_arguments


def get_environ_vars():
    user_exist = False
    pwd_exist = False
    oldpwd_exist = False
    list_vars = [None, None, None]

    if "USER" in environ:
        user_exist = True
        list_vars[0] = environ["USER"]
    if "PWD" in environ:
        pwd_exist = True
        list_vars[1] = environ["PWD"]
    if "OLDPWD" in environ:
        oldpwd_exist = True
        list_vars[2] = environ["OLDPWD"]

    return user_exist, pwd_exist, oldpwd_exist, list_vars


def tilde(arguments):
    user_exist, pwd_exist, oldpwd_exist, list_vars = get_environ_vars()
    tilde_arguments = tilde_expansion(arguments, pwd_exist,
                                      oldpwd_exist,
                                      list_vars[1], list_vars[2])
    return tilde_arguments
