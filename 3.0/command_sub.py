from re import sub
from subprocess import check_output


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


def search_quotes(command):
    """
    command - string
    từng string trong list commands trong hàm main
    return string đã bị thay đổi
    """
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
        final_command = search_quotes(command)
        return final_command
