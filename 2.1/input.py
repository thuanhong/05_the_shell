import readline
from os import environ, listdir
from shutil import which
from os.path import isdir, exists, expanduser
from glob import glob
from itertools import product
from re import sub
from subprocess import check_output


def get_variables(start_symbol, end_symbol):
    list_variables = []
    for key in environ:
        list_variables.append(start_symbol + key + end_symbol)
    return list_variables


def list_current_directory(everything=True):
    if everything:
        current_directory = [element for element in listdir('.')]
    else:
        current_directory = [element for element in listdir('.') if
                             (isdir(element) and exists(element))]
    return current_directory


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
    list_executable_files = ['cd', 'exit', 'export', 'unset']
    try:
        for path in environ["PATH"].split(":"):
            path += "/"
            list_paths.append(path)
    except Exception:
        pass

    for each_path in list_paths:
        find_executable_files(each_path, list_executable_files)

    return list_executable_files


def analyze_data(string, text, names):
    print_all = False
    if len(text.split("|")) > 1:
        string = "|".join(text.split("|")[:-1]) + "|"
        text = text.split("|")[-1]
        if text.startswith(" "):
            string += " "
    elif len(text.split()) > 1 or not text:
        names = list_current_directory()
        if text:
            string = " ".join(text.split()[:-1])
            text = text.split()[-1]
        else:
            print_all = True

    if text.startswith("${") and text.endswith("}"):
        names = get_variables("${", "}")
    elif text.startswith("${"):
        names = get_variables("${", "")
    elif text.startswith("$"):
        names = get_variables("$", "")
    return string, text, names, print_all


def completer(text, state):
    string = ""
    names = find_paths() + list_current_directory(False)
    string, text, names, print_all = analyze_data(string, text, names)
    if not print_all:
        options = [word for word in names if
                   word.startswith(text.replace(" ", ""))]
    if print_all:
        options = names

    for index, option in enumerate(options):
        options[index] = string + option

    try:
        return options[state]
    except IndexError:
        return None


def read_input():
    readline.set_completer(completer)
    # if 'libedit' in readline.__doc__:
    #     readline.parse_and_bind("bind ^I rl_complete")
    # else:
    #     readline.parse_and_bind("tab: complete")
    readline.parse_and_bind("tab: complete")
    raw_input = input('\033[1;31mintek-sh$\033[00m ')
    print('read:', [raw_input])
    return raw_input


# ----------------------------------------------------------------------------


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
        print(glob(arg))
        if glob(arg):
            pathname_list += sorted(glob(arg))
        elif not glob(arg) and ".*" not in arg :
            pathname_list += [arg]
    return pathname_list


# ----------------------------------------------------------------------------


def get_user_directory(username):
    user_directory = expanduser("~") + "/../" + username.split("/")[0][1:]

    if exists(user_directory) and isdir(user_directory):
        return expanduser("~") + "/../" + username[1:]

    return username


def tilde_expansion(raw_arguments,
                    user_exist, pwd_exist, oldpwd_exist,
                    user, current_dir, previous_dir):

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
    tilde_arguments = tilde_expansion(arguments, user_exist, pwd_exist,
                                      oldpwd_exist, list_vars[0],
                                      list_vars[1], list_vars[2])
    return tilde_arguments


# ----------------------------------------------------------------------------


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


def param(arguments, environ):
    for index, argument in enumerate(arguments):
        arguments[index] = handle_multi_backslash(argument)
        arguments[index] = search_quotes(arguments[index], environ)
    return arguments


# ----------------------------------------------------------------------------


def process_command(command):
    """
    #XX
    arg - type regex, dùng arg.group(x) để lấy ra string
    string thường có dạng "$(abc)"
    return string - string mới này sẽ được dùng để thay thế string command cũ trong substring
    """
    try:
        if command.group(0):
            command = command.group(0)
            if command.startswith("$("):
                command = command[2:-1]
            elif command.startswith("`"):
                command = command[1:-1]
            command = search_command_sub(command)
    except AttributeError:
        if command.startswith("$("):
            command = command[2:-1]
        elif command.startswith("`"):
            command = command[1:-1]

    command = command.split()
    if len(command) > 1:
        arguments = command[1:]
    else:
        arguments = [" "]

    command = command[0]

    return check_output([command] + arguments).decode("utf-8").replace("\n", "")


def search_command_sub(arg):
    """
    arg - type regex, dùng arg.group(x) để lấy ra substring
    substring thường có dạng "$(abc)"
    return substring bị thay đổi
    """
    try:
        for number in [1,3,4]:
            if arg.group(number):
                variable = sub(r"(?<!\\)\$\((?:(?!(?<!\\)\").)*(?<!\\)\)|(?<!\\)\`(?:(?!(?<!\\)\").)*(?<!\\)\`",
                               process_command, arg.group(number))
                return variable
    except AttributeError:
        variable = sub(r"(?<!\\)\$\((?:(?!(?<!\\)\").)*(?<!\\)\)|(?<!\\)\`(?:(?!(?<!\\)\").)*(?<!\\)\`",
                       process_command, arg)
        return variable
    return arg.group(2)


def search_quotes_2(command):
    """
    command - string
    từng string trong list commands trong hàm main
    return string đã bị thay đổi
    """
    print(command)
    variable = sub(r"((?<!\\)\"(?:(?!(?<!\\)\").)*(?<!\\)\")|((?<!\\)\'(?:(?!(?<!\\)\').)*\')|((?<!\\)\`(?:(?!(?<!\\)\").)*(?<!\\)\`)|((?<!\\)\$\((?:(?!(?<!\\)\").)*(?<!\\)\))",
                   search_command_sub, command)
    return variable


def command_sub(commands):
    """
    arguments = list of strings nhập bởi user
    thường có dạng ['command + arguments', 'command + arguments', etc.]
    return list of strings đã bị thay đổi, giữ nguyên format cũ
    Crash: Khi command rỗng
    Cần thêm tính năng nếu muốn giống shell xịn
    Lỗi: Nếu user nhập sai syntax, kết quả trả ra sẽ khác shell xịn
    """

    for command in commands:
        final_command = search_quotes_2(command)
        return final_command


# ----------------------------------------------------------------------------


def handle_input(raw_input):
    # 1:
    user_input = raw_input.split()
    print('handle 1:', user_input)

    # 2:
    if len(user_input) > 1:
        user_input = user_input[:1] + get_pathname_list(user_input[1:])
    print('handle 2:', user_input)

    # 3:
    if len(user_input) > 1:
        user_input = user_input[:1] + tilde(user_input[1:])
    print('handle 3:', user_input)

    # 4:
    if len(user_input) > 1:
        user_input = user_input[:1] + param(user_input[1:], environ)
    print('handle 4:', user_input)

    # 5:
    if user_input:
        user_input = command_sub([' '.join(user_input)])
    print('handle 5:', user_input)

    return user_input.split()
