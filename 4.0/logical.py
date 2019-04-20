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
                    # 1.1.2
                    string += '('
                    index += 1
                    braces += 1
                else:
                    # 1.1.1
                    new_input.append(string)
                    string = '('
                    index += 1
                    braces += 1
            else:
                braces -= 1
                if braces:
                    # 1.2.2
                    string += user_input[index]
                    index += 1
                else:
                    # 1.2.1
                    string += user_input[index]
                    new_input.append(string)
                    string = ''
                    index += 1
        else:
            if user_input[index] in ['|', '&'] and user_input[index] == user_input[index + 1]:
                if braces:
                    # 2.1.2
                    string += user_input[index: index + 2]
                    index += 2
                else:
                    # 2.1.1
                    new_input.append(string)
                    new_input.append(user_input[index: index + 2])
                    string = ''
                    index += 2
            else:
                # 2.2
                string += user_input[index]
                index += 1
    new_input.append(string)
    return [item.strip() for item in new_input if item.strip()]


def run_logical_operator(command_list, set_vars):
    for index, item in enumerate(command_list):
        if item not in ['&&', '||'] and not item.startswith("(") and not item.endswith(")"):
            try:
                run_command(item.split(), set_vars)
            except Exception:
                set_vars['exit_status'] = -1
        elif item not in ['&&', '||']:
            try:
                run_command((dirname(abspath(__file__)) + "/intek-sh.py " + item[1:-1] + " && exit $?").split(), set_vars)
            except Exception:
                set_vars['exit_status'] = -1
        try:
            if (not set_vars['exit_status'] and command_list[index + 1] == '||') \
                    or (set_vars['exit_status'] and command_list[index + 1] == '&&'):
                break
        except IndexError:
            pass
