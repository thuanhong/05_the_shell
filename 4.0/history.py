from re import findall


def read_history_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line[:-1] for line in file.readlines()]
    except Exception:
        return []


def save_history_file(file_path, user_input):
    try:
        with open(file_path, 'a+') as file:
            file.write(user_input + '\n')
    except Exception:
        pass


def save_input(file_path, set_vars, user_input):
    if user_input:
        save_history_file(file_path, user_input)
        set_vars['history'].append(user_input)


def print_all_history(history_content):
    tab = len(str(len(history_content)))
    for line, content in enumerate(history_content, 1):
        print('{}{}  {}'.format(
            (tab - len(str(line)) + 2) * ' ',
            line,
            content))


def print_part_history(history_content, number):
    tab = len(str(len(history_content)))
    start = len(history_content) - number
    for line, content in enumerate(history_content[start:], start + 1):
        print('{}{}  {}'.format(
            (tab - len(str(line)) + 2) * ' ',
            line,
            content))


def show_history(arguments, set_vars):
    if set_vars['history']:
        if arguments and int(arguments[0]) < len(set_vars['history']):
            print_part_history(set_vars['history'], int(arguments[0]))
        else:
            print_all_history(set_vars['history'])


def find_command_history(user_input, set_vars):
    try:
        user_input = user_input.replace('!!', set_vars['history'][-1])
    except IndexError:
        pass
    for command in findall('\!\d+', user_input):
        try:
            user_input = user_input.replace(
                command, set_vars['history'][int(command[1:]) - 1])
        except IndexError:
            continue
    return user_input
