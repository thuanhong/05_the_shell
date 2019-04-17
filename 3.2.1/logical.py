from command import run_command
from re import split


# def split_logical_operator(user_input):
#     return split(r"(&&)\s*(?![^()]*\))|(\|\|)\s*(?![^()]*\))", user_input)


def check_nearest(num, num_list):
    num_list = [i for i in num_list if i != -1]
    if num_list:
        return num < min(num_list)
    return not num == -1


def split_logical_operator(user_input):
    new_input = []
    if user_input:
        a = user_input.find('&&')
        b = user_input.find('||')
        c = user_input.find('(')
        d = user_input.rfind(')')

        if check_nearest(a, [b, c]):
            new_input.append(user_input[:a])
            new_input.append('&&')
            new_input += split_logical_operator(user_input[a + 2:])
        elif check_nearest(b, [a, c]):
            new_input.append(user_input[:b])
            new_input.append('||')
            new_input += split_logical_operator(user_input[b + 2:])
        elif check_nearest(c, [a, b]):
            new_input.append(user_input[c:d + 1])
            new_input += split_logical_operator(user_input[d + 1:])
        else:
            new_input.append(user_input)
    return new_input


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
