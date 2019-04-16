#!/usr/bin/env python3
from subprocess import run


def check_nested_list(item):
    for element in item:
        if isinstance(element, list):
            return True
    return False


def recursive(command_list):
    exit_status = 0
    for index, item in enumerate(command_list):
        if item not in [['&&'], ['||']]:
            if check_nested_list(item):
                exit_status = recursive(item)
            else:
                exit_status = run(item).returncode
            try:
                if not exit_status and command_list[index + 1] == ['||'] \
                        or exit_status and command_list[index + 1] == ['&&']:
                    break
            except IndexError:
                pass
    return exit_status


def main():
    command_list = [['echo', 'hello A'],
                    ['||'],
                    [['echo', 'hello B1'], ['||'], ['echo', 'hello B2']],
                    ['&&'],
                    [[['echo', 'hello C11'], ['&&'], ['echo', 'hello C12']], ['||'], ['echo', 'hello C2']]]
    recursive(command_list)


if __name__ == '__main__':
    main()
