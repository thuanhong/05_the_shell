from re import sub
from subprocess import check_output
from globbing import get_pathname_list


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
        arguments = get_pathname_list(" ".join(arguments)).split()
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
                print("hello", arg.group(number))
                variable = sub(r"(?<!\\)\$\((?:(?!(?<!\\)\").)*(?<!\\)\)|(?<!\\)\`(?:(?!(?<!\\)\").)*(?<!\\)\`",
                               process_command, arg.group(number))
                print(variable)
                return variable
    except AttributeError:
        print("hi", arg)
        variable = sub(r"(?<!\\)\$\((?:(?!(?<!\\)\").)*(?<!\\)\)|(?<!\\)\`(?:(?!(?<!\\)\").)*(?<!\\)\`",
                       process_command, arg)
        print(variable)
        return variable
    return arg.group(2)


def command_sub(command):
    """
    command - string
    từng string trong list commands trong hàm main
    return string đã bị thay đổi
    """
    variable = sub(r"((?<!\\)\"(?:(?!(?<!\\)\").)*(?<!\\)\")|((?<!\\)\'(?:(?!(?<!\\)\').)*\')|((?<!\\)\`(?:(?!(?<!\\)\").)*(?<!\\)\`)|((?<!\\)\$\((?:(?!(?<!\\)\").)*(?<!\\)\))",
                   search_command_sub, command)
    return variable
