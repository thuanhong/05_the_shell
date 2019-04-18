from command import run_command
from re import split


def split_logical_operator(user_input):
    new_input = split(r"(\((?:[^\}]*)\))|(&&)\s*(?![^()]*\))|(\|\|)\s*(?![^()]*\))", user_input)
    return [item.strip(' ') for item in new_input if item and item.strip(' ')]


def run_logical_operator(command_list, set_vars):
    for index, item in enumerate(command_list):
        if item not in ['&&', '||'] and not item.startswith("(") and not item.endswith(")"):
            try:
                run_command(item.split(), set_vars)
            except Exception:
                set_vars['exit_status'] = -1
        elif item not in ['&&', '||']:
            try:
                run_command(("./intek-sh.py " + item[1:-1] + " && exit $?").split(), set_vars)
            except Exception:
                set_vars['exit_status'] = -1
        try:
            if (not set_vars['exit_status'] and command_list[index + 1] == '||') \
                    or (set_vars['exit_status'] and command_list[index + 1] == '&&'):
                break
        except IndexError:
            pass
