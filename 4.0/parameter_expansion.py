from os import environ
from re import sub


def replace_variable(substring):
    """
    Search if $variable is in the shell's variable or not
    if True, replace it with its value
    """
    if substring.group(2):
        substring = substring.group(2)
        if substring == "$":
            return "$"
        # replace with its value
        elif substring[1:] in set_variables:
            return set_variables[substring[1:]]
        # replace with exit status
        elif substring[1:] == "?":
            return str(set_variables['exit_status'])
        else:
            return ""
    # ignore what is in subshell
    elif substring.group(1):
        return substring.group(1)


def change_user_input(user_input):
    """
    Search for $variable and $variable inside subshell
    Replace them with their value if need

    Return their value
    """
    # inside subshell
    pattern1 = r"((?<!\\)\((?:(?!(?<!\\)\)).)*(?<!\\)\))|"
    # catch all $variable
    pattern2 = r"(?<!\\)((?:|(?<=(\s)))\$[\d\w\?]*)"
    user_input = sub(pattern1 + pattern2,
                     replace_variable, user_input)
    return user_input


def get_param_and_word(variable, substring):
    """
    Split string by a defined symbol
    """
    # first index become parameter (key)
    parameter = variable.split(substring, 1)[0]
    # second index become word (value)
    if len(variable.split(substring, 1)) > 1:
        word = variable.split(substring, 1)[1]
    else:
        word = ""
    return parameter, word


def getVar(variable):
    """
    Depend on the symbol between parameter(key) and word(value)
    Get the correct string from the parameter expansion

    return a string, the result of parameter expansion
    """
    # remove brackets
    try:
        if variable.group(0):
            variable = variable.group(0)
            variable = variable[2:-1]
            variable = search_bracket(variable)
    except AttributeError:
        variable = variable[2:-1]
    if variable in set_variables:
        return set_variables[variable]
    elif variable.startswith("#"):
        # return len of parameter
        if variable[1:] in set_variables:
            return str(len(set_variables[variable[1:]]))
        else:
            return "0"
    elif ":-" in variable:
        parameter, word = get_param_and_word(variable, ":-")
        # substitute parameter
        if parameter in set_variables and set_variables[parameter]:
            return set_variables[parameter]
        # substitute word
        elif (parameter not in set_variables or
              (parameter in set_variables and not set_variables[parameter])):
            return word
    elif "-" in variable:
        # substitute parameter
        parameter, word = get_param_and_word(variable, "-")
        if parameter in set_variables and Sset_variables[parameter]:
            return set_variables[parameter]
        # substitute null
        elif parameter in set_variables and not set_variables[parameter]:
            return ""
        # substitute word
        elif parameter not in set_variables:
            return word
    elif ":=" in variable:
        parameter, word = get_param_and_word(variable, ":=")
        # substitute parameter
        if parameter in set_variables and set_variables[parameter]:
            return set_variables[parameter]
        # assign word
        elif (parameter not in set_variables or
              (parameter in set_variables and not set_variables[parameter])):
            set_variables[parameter] = word
            return word
    elif "=" in variable:
        parameter, word = get_param_and_word(variable, "=")
        # substitute parameter
        if parameter in set_variables and set_variables[parameter]:
            return set_variables[parameter]
        # substitute null
        elif parameter in set_variables and not set_variables[parameter]:
            return ""
        # assign word
        elif parameter not in set_variables:
            set_variables[parameter] = word
            return word
    elif ":+" in variable:
        parameter, word = get_param_and_word(variable, ":+")
        # substitute word
        if parameter in set_variables:
            return word
        # substitute null
        elif parameter in set_variables and not set_variables[parameter]:
            return ""
        # substitute null
        elif parameter not in set_variables:
            return ""
    elif "+" in variable:
        parameter, word = get_param_and_word(variable, "+")
        # substitute word
        if (parameter in set_variables or
           (parameter in set_variables and not set_variables[parameter])):
            return word
        # substitute null
        elif parameter not in set_variables:
            return ""
    elif "%" in variable:
        variable = variable.replace("%", " ")
        parameter, word = get_param_and_word(variable, None)
        # substitute parameter
        if (parameter in set_variables and
           (not set_variables[parameter].endswith(word) or not word)):
            return set_variables[parameter]
        # remove 'word' from the ending of parameter
        if (parameter in set_variables and
           set_variables[parameter].endswith(word) and
           set_variables[parameter]):
            return set_variables[parameter][:-len(word)]
        # substitute null
        elif (parameter not in set_variables or
              (parameter in set_variables and not set_variables[parameter])):
            return ""
    elif "#" in variable:
        variable = variable.replace("#", " ")
        parameter, word = get_param_and_word(variable, None)
        # substitute parameter
        if (parameter in set_variables and
           (not set_variables[parameter].startswith(word) or not word)):
            return set_variables[parameter]
        # remove 'word' from the beginning of parameter
        if (parameter in set_variables and
           set_variables[parameter].startswith(word) and
           set_variables[parameter]):
            return set_variables[parameter][len(word):]
        # substitute null
        elif (parameter not in set_variables or
              (parameter in set_variables and not set_variables[parameter])):
            return ""
    if variable not in set_variables:
        # variable doesn't have a value, substitute null
        return ""


def search_bracket(argument):
    """
    Recursively search for brackets and nested brackets
    And change parameter follow user's wish

    Return parameter value if any is substituted
    """
    try:
        for number in [1, 3, 5]:
            if argument.group(number):
                # search for brackets and nested brackets
                variable = sub(r"(?<!\\)\$\{(?:(?!(?<!\\)\").)*(?<!\\)\}",
                               getVar, argument.group(number))
                return variable
    except AttributeError:
        # do substitution
        variable = sub(r"(?<!\\)\$\{(?:(?!(?<!\\)\").)*(?<!\\)\}",
                       getVar, argument)
        return variable
    # return the parameter its self, no substitution made
    if argument.group(2):
        return argument.group(2)
    elif argument.group(4):
        return argument.group(4)


def search_quotes(argument):
    """
    Search for ouside brackets, ignore quotes, escaped and subshell
    """
    # inside quotes
    pattern1 = r"((?<!\\)\"(?:(?!(?<!\\)\").)*(?<!\\)\")|"
    pattern2 = r"((?<!\\)\'(?:(?!(?<!\\)\').)*\')|"
    # inside $() - command substitution
    pattern3 = r"((?<!\\)\$\((?:(?!(?<!\\)\)).)*(?<!\\)\))|"
    # inside () - subshell
    pattern4 = r"((?<!\\)\((?:(?!(?<!\\)\)).)*(?<!\\)\))|"
    # inside ${} - parameter substitution
    pattern5 = r"((?<!\\)\$\{(?:(?!(?<!\\)\}).)*(?<!\\)\})"
    variable = sub(pattern1 + pattern2 + pattern3 + pattern4 +
                   pattern5, search_bracket, argument)
    return variable


def expanse_parameter(argument):
    """
    Search for parameter expansion to do substitution

    Return user's input after expansion
    """
    argument = search_quotes(argument)
    return argument
