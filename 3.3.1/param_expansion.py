from os import environ
from re import sub


def replace_variable(substring):

    substring = substring.group(0)
    if substring == "$":
        return "$"
    elif substring[1:] in set_variables:
        return set_variables[substring[1:]]
    else:
        return ""


def change_user_input(user_input):
    user_input  = sub(r"(?:|(?<=(\s)))\$[\d\w]*", replace_variable, user_input)
    return user_input


def get_param_and_word(variable, substring):
    """
    variable = string
    ví dụ: 'abc:=HOME'  hoặc 'abc:+PWD' hoặc 'abc%%USER'
    substring = string - các kí tự đặc biệt nằm giữa string
    ví dụ:  ':=' hoặc ':+' hoặc '%%'
    return 2 string mới ( string cũ cắt đôi)
    """

    parameter = variable.split(substring, 1)[0]
    if len(variable.split(substring, 1)) > 1:
        word = variable.split(substring, 1)[1]
    else:
        word = ""

    return parameter, word


def getVar(variable):
    """
    variable = string
    sub-substring mới này sẽ được dùng để thay thế chính nó trong substring cũ
    """

    try:
        if variable.group(0):
            variable = variable.group(0)
            variable = variable[2:-1]
            variable = search_bracket(variable)
    except AttributeError:
        variable = variable[2:-1]

    if variable in set_variables:
        variable = set_variables[variable]

    elif variable.startswith("#"):
        if variable[1:] in set_variables:
            variable = str(len(set_variables[variable[1:]]))
        else:
            variable = "0"

    elif ":-" in variable:
        parameter, word = get_param_and_word(variable, ":-")
        if parameter in set_variables and set_variables[parameter]:
            variable = set_variables[parameter]
        elif parameter not in set_variables or (parameter in set_variables and not set_variables[parameter]):
            variable = word

    elif "-" in variable:
        parameter, word = get_param_and_word(variable, "-")
        if parameter in set_variables and Sset_variables[parameter]:
            variable = set_variables[parameter]
        elif parameter in set_variables and not set_variables[parameter]:
            variable = ""
        elif parameter not in set_variables:
            variable = word

    elif ":=" in variable:
        parameter, word = get_param_and_word(variable, ":=")
        if parameter in set_variables and set_variables[parameter]:
            variable = set_variables[parameter]
        elif parameter not in set_variables or (parameter in set_variables and not set_variables[parameter]):
            variable = word
            set_variables[parameter] = word

    elif "=" in variable:
        parameter, word = get_param_and_word(variable, "=")
        if parameter in set_variables and set_variables[parameter]:
            variable = set_variables[parameter]
        elif parameter in set_variables and not set_variables[parameter]:
            variable = ""
        elif parameter not in set_variables:
            variable = word
            set_variables[parameter] = word

    elif ":+" in variable:
        parameter, word = get_param_and_word(variable, ":+")
        if parameter in set_variables:
            variable = word
        elif parameter in set_variables and not set_variables[parameter]:
            variable = ""
        elif parameter not in set_variables:
            variable = ""

    elif "+" in variable:
        parameter, word = get_param_and_word(variable, "+")
        if parameter in set_variables or (parameter in set_variables and not set_variables[parameter]):
            variable = word
        elif parameter not in set_variables:
            variable = ""

    elif "%" in variable:
        variable = variable.replace("%", " ")
        parameter, word = get_param_and_word(variable, None)
        if parameter in set_variables and (not set_variables[parameter].endswith(word) or not word):
            variable = set_variables[parameter]
        if parameter in set_variables and set_variables[parameter].endswith(word) and set_variables[parameter] :
            variable = set_variables[parameter][:-len(word)]
        elif parameter not in set_variables or (parameter in set_variables and not set_variables[parameter]):
            variable = ""

    elif "#" in variable:
        variable = variable.replace("#", " ")
        parameter, word = get_param_and_word(variable, None)
        if parameter in set_variables and (not set_variables[parameter].startswith(word) or not word):
            variable = set_variables[parameter]
        if parameter in set_variables and set_variables[parameter].startswith(word) and set_variables[parameter]:
            variable = set_variables[parameter][len(word):]
        elif parameter not in set_variables or (parameter in set_variables and not set_variables[parameter]):
            variable = ""

    return variable


def search_bracket(arg):
    """
    arg - type regex, sẽ dùng lệnh arg.group(x) để lấy ra dưỡi dạng substring   "${abc=HOME}"
    return lại substring đó nhưng đã bị thay đổi
    """
    try:
        for number in [1,3]:
            if arg.group(number):
                variable = sub(r"(?<!\\)\$\{(?:(?!(?<!\\)\").)*(?<!\\)\}",
                               getVar, arg.group(number))
                return variable
    except AttributeError:
        variable = sub(r"(?<!\\)\$\{(?:(?!(?<!\\)\").)*(?<!\\)\}", getVar, arg)
        return variable
    return arg.group(2)


def search_quotes(arg, set_vars):
    """
    argument = string
    thường có dạng 'command + arguments'
    return string trên sau khi sửa đổi
    """

    variable = sub(r"((?<!\\)\"(?:(?!(?<!\\)\").)*(?<!\\)\")|((?<!\\)\'(?:(?!(?<!\\)\').)*\')|((?<!\\)\$\{(?:(?!(?<!\\)\").)*(?<!\\)\})",
                   search_bracket, arg)
    return variable


def handle_multi_backslash(argument):
    """
    argument = string
    thường có dạng 'command + arguments'
    return string trên nhưng đã được sửa đổi
    """

    if r"\\" in argument:
        argument = argument.replace(r"\\",r"")

    return argument


def param(argument):
    argument = handle_multi_backslash(argument)
    argument = search_quotes(argument, environ)
    return argument
