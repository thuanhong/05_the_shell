from command import run_command
from os.path import dirname, abspath


def split_logical_operator(user_input):
    """
    Split user's input into logical operators

    @param: user_input: user's input

    @return: new_input: (list) input after split logical operators
    """
    new_input = []
    index, braces, string = 0, 0, ''
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


def is_unvalid(command_list, set_variables, index):
    """
    Check command is unvalid

    @param command_list: list of commands
    @param set_variables: dictionary of variables
    @param index:

    @return: True if unvalid command, False if valid command
    """
    return ((set_variables['exit_status'] == 0 and
             command_list[index - 1] == '||')
            or (set_variables['exit_status'] != 0 and
                command_list[index - 1] == '&&'))


def control_execute_command(set_variables, command):
    """
    Execute command

    @param set_variables: dictionary of variables
    @param command: user's command
    """
    if command.startswith('(') and command.endswith(')'):
        command = ("python3 " + dirname(abspath(__file__)) + "/intek-sh.py "
                   + command[1:-1] + " && exit $?")
        run_command(command.split(), set_variables)
    elif command not in ['&&', '||']:
        run_command(command.split(), set_variables)


def run_logical_operator(command_list, set_variables):
    """
    Check if the command is executable

    @param command_list: list of commands
    @param set_variables: dictionary of variables
    """
    for index, item in enumerate(command_list):
        if index == 0:
            control_execute_command(set_variables, item)
        elif not is_unvalid(command_list, set_variables, index):
            control_execute_command(set_variables, item)
