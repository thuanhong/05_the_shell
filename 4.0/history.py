from re import findall


def read_history_file(file_path):
    """
    Read history file

    @param file_path: path to history file

    @return: list of commands
    """
    try:
        with open(file_path, 'r') as file:
            return [line[:-1] for line in file.readlines()]
    except Exception:
        return []


def save_history_file(file_path, user_input):
    """
    Write to history file

    @param file_path: path to history file
    @param user_input: user's input
    """
    try:
        with open(file_path, 'a+') as file:
            file.write(user_input + '\n')
    except Exception:
        pass


def save_input(file_path, set_variables, user_input):
    """
    Save input

    @param file_path: path to history file
    @param set_variables: dictionary of variables
    @param user_input: user's input
    """
    if user_input:
        save_history_file(file_path, user_input)
        set_variables['history'].append(user_input)


def print_all_history(history_content):
    """
    Display history to screen

    @param history_content: list of history content
    """
    tab = len(str(len(history_content)))
    for line, content in enumerate(history_content, 1):
        print('{}{}  {}'.format(
            (tab - len(str(line)) + 2) * ' ',
            line,
            content))


def print_part_history(history_content, number):
    """
    Display part of history to screen

    @param history_content: list of history content
    @param number: number of lines
    """
    tab = len(str(len(history_content)))
    start = len(history_content) - number
    for line, content in enumerate(history_content[start:], start + 1):
        print('{}{}  {}'.format(
            (tab - len(str(line)) + 2) * ' ',
            line,
            content))


def show_history(arguments, set_variables):
    """
    Control the behaviour of functions
    print_all_history and print_part_history

    @param arguments: list of arguments
    @param set_variables: dictionary of variables
    """
    if set_variables['history']:
        if arguments and int(arguments[0]) < len(set_variables['history']):
            print_part_history(set_variables['history'], int(arguments[0]))
        else:
            print_all_history(set_variables['history'])


def find_command_history(user_input, set_variables):
    """
    Find command base on its index

    @param user_input: user's input
    @param set_variables: dictionary of variables

    @return: command found
    """
    try:
        user_input = user_input.replace('!!', set_variables['history'][-1])
    except IndexError:
        pass
    for command in findall('\!\d+', user_input):
        try:
            user_input = user_input.replace(
                command, set_variables['history'][int(command[1:]) - 1])
        except IndexError:
            continue
    return user_input
