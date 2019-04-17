from command import run_command
from re import split


def split_logical_operator(user_input):
    user_input = split(r"(&&)\s*(?![^()]*\))|(\|\|)\s*(?![^()]*\))", user_input)
    return [item.split() for item in user_input if item]


def run_logical_operator(command_list, set_vars):
    for index, item in enumerate(command_list):
        if item not in [['&&'], ['||']]:
            try:
                run_command(item, set_vars)
            except Exception:
                set_vars['exit_status'] = -1
        try:
            if (not set_vars['exit_status'] and command_list[index + 1] == ['||']) \
                    or (set_vars['exit_status'] and command_list[index + 1] == ['&&']):
                break
        except IndexError:
            pass
