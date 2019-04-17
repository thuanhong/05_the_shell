from command import run_command


def check_nested_list(item):
    for element in item:
        if isinstance(element, list):
            return True
    return False


def recursive_logical(command_list, set_vars):
    for index, item in enumerate(command_list):
        if item not in [['&&'], ['||']]:
            try:
                if check_nested_list(item):
                    recursive_logical(item, set_vars)
                else:
                    run_command(item, set_vars)
            except Exception:
                set_vars['exit_status'] = -1
            try:
                if not set_vars['exit_status'] and command_list[index + 1] == ['||'] \
                        or set_vars['exit_status'] and command_list[index + 1] == ['&&']:
                    break
            except IndexError:
                pass
    return set_vars['exit_status']
