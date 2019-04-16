from os import environ
from re import sub


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

    ltVars = environ
    try:
        if variable.group(0):
            variable = variable.group(0)
            variable = variable[2:-1]
            variable = search_bracket(variable)
    except AttributeError:
        variable = variable[2:-1]

    if variable in ltVars:
        variable = ltVars[variable]

    elif variable.startswith("#"):
        if "=" in variable:
            print("intek-sh: bad substitution")
            exit()
        if variable[1:] in ltVars:
            variable = str(len(ltVars[variable[1:]]))
        else:
            variable = "0"

    elif ":-" in variable:
        parameter, word = get_param_and_word(variable, ":-")
        if parameter in ltVars and ltVars[parameter]:
            variable = ltVars[parameter]
        elif parameter not in ltVars or (parameter in ltVars and not ltVars[parameter]):
            variable = word

    elif "-" in variable:
        parameter, word = get_param_and_word(variable, "-")
        if parameter in ltVars and ltVars[parameter]:
            variable = ltVars[parameter]
        elif parameter in ltVars and not ltVars[parameter]:
            variable = ""
        elif parameter not in ltVars:
            variable = word

    elif ":=" in variable:
        parameter, word = get_param_and_word(variable, ":=")
        if parameter in ltVars and ltVars[parameter]:
            variable = ltVars[parameter]
        elif parameter not in ltVars or (parameter in ltVars and not ltVars[parameter]):
            variable = word

        ##############################
        #                            #
        #  goi ham de set(variable)  #
        #                            #
        ##############################

    elif "=" in variable:
        parameter, word = get_param_and_word(variable, "=")
        if parameter in ltVars and ltVars[parameter]:
            variable = ltVars[parameter]
        elif parameter in ltVars and not ltVars[parameter]:
            variable = ""
        elif parameter not in ltVars:
            variable = word

        ##############################
        #                            #
        #  goi ham de set(variable)  #
        #                            #
        ##############################

    elif ":+" in variable:
        parameter, word = get_param_and_word(variable, ":+")
        if parameter in ltVars:
            variable = word
        elif parameter in ltVars and not ltVars[parameter]:
            variable = ""
        elif parameter not in ltVars:
            variable = ""

    elif "+" in variable:
        parameter, word = get_param_and_word(variable, "+")
        if parameter in ltVars or (parameter in ltVars and not ltVars[parameter]):
            variable = word
        elif parameter not in ltVars:
            variable = ""

    elif "%" in variable:
        variable = variable.replace("%", " ")
        parameter, word = get_param_and_word(variable, None)
        if parameter in ltVars and (not ltVars[parameter].endswith(word) or not word):
            variable = ltVars[parameter]
        if parameter in ltVars and ltVars[parameter].endswith(word) and ltVars[parameter] :
            variable = ltVars[parameter][:-len(word)]
        elif parameter not in ltVars or (parameter in ltVars and not ltVars[parameter]):
            variable = ""

    elif "#" in variable:
        variable = variable.replace("#", " ")
        parameter, word = get_param_and_word(variable, None)
        if parameter in ltVars and (not ltVars[parameter].startswith(word) or not word):
            variable = ltVars[parameter]
        if parameter in ltVars and ltVars[parameter].startswith(word) and ltVars[parameter]:
            variable = ltVars[parameter][len(word):]
        elif parameter not in ltVars or (parameter in ltVars and not ltVars[parameter]):
            variable = ""

    elif ":" in variable:
        parameter, word = get_param_and_word(variable, ":")
        if parameter in ltVars and word.isnumeric():
            variable = ltVars[parameter][int(word):]
        elif parameter in ltVars and not word:
            print("intek-sh: bad substitution")
            exit()
        elif parameter in ltVars and not word.isnumeric():
            variable = ltVars[parameter]
        elif parameter not in ltVars:
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


def search_quotes(arg, ltVars):
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


def param(arguments):
    for index, argument in enumerate(arguments):
        arguments[index] = handle_multi_backslash(argument)
        arguments[index] = search_quotes(arguments[index], environ)
    return arguments
