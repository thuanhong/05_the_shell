from re import sub
from subprocess import check_output
from globbing import get_pathname_list


def remove_quotes(substring):
    # return substring without the starting and ending character
    return substring.group(0)[1:-1]


def process_command(command):
    """
    Turn string inside $() or `` into "command + arguments"
    Then run that command
    And return that command's output
    """
    try:
        if command.group(0):
            command = command.group(0)
            # remove unused symbols
            if command.startswith("$("):
                command = command[2:-1]
            elif command.startswith("`"):
                command = command[1:-1]
            # recursively search for nested command substution
            command = search_command_sub(command)
    except AttributeError:
        # stop the recursion
        if command.startswith("$("):
            command = command[2:-1]
        elif command.startswith("`"):
            command = command[1:-1]
    command = command.split()
    if len(command) > 1:
        # create list of arguments
        arguments = command[1:]
        arguments = get_pathname_list(" ".join(arguments)).split()
    else:
        # no argument
        arguments = [" "]
    command = command[0]
    # get output
    output = check_output([command] + arguments).decode("utf-8")
    # remove all line-break from output
    return output.replace("\n", "")


def search_command_sub(arg):
    """
    Search for command-subs nested inside quotes
    Change them to usable strings

    @param arg: type regex, arg.group(0) is a substring

    Return substring that already changed
    """
    # inside $()
    regex_pattern1 = r"(?<!\\)\$\((?:(?!(?<!\\)\").)*(?<!\\)\)|"
    # inside backquotes
    regex_pattern2 = r"(?<!\\)\`(?:(?!(?<!\\)\").)*(?<!\\)\`"
    try:
        # recursively find for deep-level nested:
        for number in [1, 3, 4]:
            if arg.group(number):
                variable = sub(regex_pattern1 + regex_pattern2,
                               process_command, arg.group(number))
                return variable
    except AttributeError:
        # stop recursion
        variable = sub(regex_pattern1 + regex_pattern2,
                       process_command, arg)
        return variable
    # return it-self if it's an invalid command-sub
    if arg.group(2):
        return arg.group(2)
    elif arg.group(5):
        return arg.group(5)


def command_sub(command):
    """
    Search for quotes, subshell, and valid command-subs
    Change command-subs into usable strings

    @param command: string, user's input

    Return the whole string that already changed
    """
    # inside quotes
    regex_pattern1 = r"((?<!\\)\"(?:(?!(?<!\\)\").)*(?<!\\)\")|"
    regex_pattern2 = r"((?<!\\)\'(?:(?!(?<!\\)\').)*\')|"
    # inside backquotes and $()
    regex_pattern3 = r"((?<!\\)\`(?:(?!(?<!\\)\`).)*(?<!\\)\`)|"
    regex_pattern4 = r"((?<!\\)\$\((?:(?!(?<!\\)\)).)*(?<!\\)\))|"
    # inside ()
    regex_pattern5 = r"((?<!\\)\((?:(?!(?<!\\)\)).)*(?<!\\)\))"
    user_command = (sub(regex_pattern1 + regex_pattern2 +
                        regex_pattern3 + regex_pattern4 +
                        regex_pattern5,
                    search_command_sub, command))
    # Find and remove all quotes
    # inside double quotes
    pattern1 = r"((?<!\\)\"(?:(?!(?<!\\)\").)*(?<!\\)\")|"
    # inside single quotes
    pattern2 = r"((?<!\\)\'(?:(?!(?<!\\)\').)*\')"
    user_command = sub(pattern1 + pattern2,
                       remove_quotes, user_command)
    return user_command
