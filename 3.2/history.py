def save_input(set_vars, uset_input):
    if uset_input:
        set_vars['history'].append(uset_input)


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
    return user_input
