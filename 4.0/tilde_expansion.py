from os.path import expanduser, exists, isdir
from os import environ


def get_user_directory(username):
    """
    Get the absolute path to user's directory

    return that path
    """
    user_directory = expanduser("~") + "/../" + username.split("/")[0][1:]
    # Only if this directory exists
    if exists(user_directory) and isdir(user_directory):
        return expanduser("~") + "/../" + username[1:]
    return username


def tilde_expansion(raw_arguments,
                    pwd_exist, oldpwd_exist,
                    current_dir, previous_dir):
    """
    Expanse the path depends on user's input
    Return path after expansion
    """
    for index, argument in enumerate(raw_arguments):
        # Expanse to home directory
        if argument == "~" or argument.startswith("~/"):
            raw_arguments[index] = expanduser(argument)
        # Expanse to current directory
        elif pwd_exist and argument == "~+":
            raw_arguments[index] = current_dir
        elif pwd_exist and argument.startswith("~+"):
            raw_arguments[index] = current_dir + argument[2:]
        # Expanse to previous directory
        elif oldpwd_exist and argument == "~-":
            raw_arguments[index] = previous_dir
        elif oldpwd_exist and argument.startswith("~-"):
            raw_arguments[index] = previous_dir + argument[2:]
        # Expanse to user directory
        elif (argument.startswith("~") and not
              argument.startswith("~-") and not argument.startswith("~+")):
            raw_arguments[index] = get_user_directory(argument)
    return raw_arguments


def get_environ_variables():
    """
    Get value of loguser, current directory, and previous directory
    inside environ

    Return those value
    """
    # Default : They dont exist
    user_exist = False
    pwd_exist = False
    oldpwd_exist = False
    list_vars = [None, None, None]
    # If they exist, get their value
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


def expanse_tilde(arguments):
    """
    Turn "~" to a meaningful path
    Solve: ~ ; ~+ ; ~-
    """
    arguments = arguments.split()
    user_exist, pwd_exist, oldpwd_exist, list_vars = get_environ_variables()
    arguments = tilde_expansion(arguments, pwd_exist,
                                oldpwd_exist,
                                list_vars[1], list_vars[2])
    return " ".join(arguments)
