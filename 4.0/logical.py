from command import run_command
from os.path import dirname, abspath


def split_logical_operator(user_input):
    new_input = []
    index, braces = 0, 0
    string = ''

    while index < len(user_input):
        if user_input[index] in ['(', ')']:
            if user_input[index] == '(':
                if braces:
                    string += '('
                else:
                    new_input.append(string)
                    string = '('
                braces += 1
            else:
                braces -= 1
                string += user_input[index]
                if not braces:
                    new_input.append(string)
                    string = ''
        else:
            try:
                if (user_input[index] in ['|', '&'] and
                        user_input[index] == user_input[index + 1]):
                    if braces:
                        string += user_input[index: index + 2]
                    else:
                        new_input += [string, user_input[index: index + 2]]
                        string = ''
                    index += 1
                else:
                    string += user_input[index]
            except IndexError:
                pass
        index += 1
    new_input.append(string)
    return [item.strip() for item in new_input if item.strip()]


def check_command_validation(command_list, set_vars, index):
    return ((set_vars['exit_status'] == 0 and
             command_list[index - 1] == '||')
            or (set_vars['exit_status'] != 0 and
                command_list[index - 1] == '&&'))


def control_execute_command(set_vars, command):
    if command.startswith('(') and command.endswith(')'):
        command = (dirname(abspath(__file__)) + "/intek-sh.py "
                   + command[1:-1] + " && exit $?")
        run_command(command.split(), set_vars)
    elif command not in ['&&', '||']:
        run_command(command.split(), set_vars)


def run_logical_operator(command_list, set_vars):
    for index, item in enumerate(command_list):
        if index == 0:
            control_execute_command(set_vars, item)
        elif not check_command_validation(command_list, set_vars, index):
            control_execute_command(set_vars, item)
