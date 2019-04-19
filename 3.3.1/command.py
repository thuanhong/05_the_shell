from os import environ, chdir, getcwd
from os.path import exists, isfile, isdir, join
from subprocess import run
from history import show_history


def check_and_move_dir(path, set_vars):
    if isdir(path):
        chdir(path)
        export_variable(['PWD=' + getcwd()], set_vars)
        set_vars['exit_status'] = 0
    elif isfile(path):
        print('intek-sh: cd: ' + path + ': Not a directory')
        set_vars['exit_status'] = 1
    else:
        print('intek-sh: cd: ' + path + ': No such file or directory')
        set_vars['exit_status'] = 1


def change_current_dir(arguments, set_vars):
    if arguments:
        check_and_move_dir(arguments[0], set_vars)
    else:
        if 'HOME' in set_vars:
            check_and_move_dir(set_vars['HOME'], set_vars)
        else:
            print('intek-sh: cd: HOME not set')
            set_vars['exit_status'] = 1


def print_env_variable(arguments, set_vars):
    if arguments:
        error_flag = False
        for arg in arguments:
            if arg in environ:
                print(environ[arg])
            else:
                error_flag = True
        if error_flag:
            set_vars['exit_status'] = 1
        else:
            set_vars['exit_status'] = 0
    else:
        for key, value in environ.items():
            print(key + '=' + value)
        set_vars['exit_status'] = 0


def export_variable(arguments, set_vars):
    if arguments:
        for arg in arguments:
            if arg[0].isnumeric() or arg.startswith('='):
                print("intek-sh: export: `" + arg +
                      "': not a valid identifier")
                set_vars['exit_status'] = 1
            elif '=' in arg:
                pos = arg.find('=')
                environ[arg[:pos]] = arg[pos + 1:]
                set_vars[arg[:pos]] = arg[pos + 1:]
                set_vars['exit_status'] = 0
    else:
        for key, value in sorted(environ.items()):
            print('export ' + key + '=' + value)
        set_vars['exit_status'] = 0


def unset_variable(arguments, set_vars):
    for arg in arguments:
        if arg[0].isnumeric() or arg.startswith('='):
            print("intek-sh: unset: `" + arg + "': not a valid identifier")
            set_vars['exit_status'] = 1
        elif arg in set_vars:
            try:
                del environ[arg]
            except KeyError:
                pass
            del set_vars[arg]
            set_vars['exit_status'] = 0


def exit_shell(arguments, set_vars):
    if arguments:
        try:
            if isinstance(int(arguments[0]), int):
                if len(arguments) == 1:
                    set_vars['exit_status'] = int(arguments[0]) % 256
                    exit(set_vars['exit_status'])
                else:
                    print('intek-sh: exit: too many arguments')
                    set_vars['exit_status'] = 1
        except ValueError:
            print('intek-sh: exit: ' + arguments[0] +
                  ': numeric argument required')
            set_vars['exit_status'] = 2
    else:
        set_vars['exit_status'] = 0
        exit()


def display_history(arguments, set_vars):
    if not arguments:
        show_history(arguments, set_vars)
        set_vars['exit_status'] = 0
    elif len(arguments) == 1 and arguments[0].isnumeric():
        show_history(arguments, set_vars)
        set_vars['exit_status'] = 0
    else:
        if not arguments[0].isnumeric():
            print('intek-sh: history: ' + arguments[0] +
                  ': numeric argument required')
        else:
            print('intek-sh: history: too many arguments')
        set_vars['exit_status'] = 1


def get_command_path(command, set_vars):
    for path in set_vars['PATH'].split(':'):
        command_path = join(path, command)
        if exists(command_path):
            return command_path


def check_and_run_command(command, arguments, set_vars):
    try:
        set_vars['exit_status'] = run([command] + arguments).returncode
    except PermissionError:
        print('intek-sh: ' + command + ': Permission denied')
        set_vars['exit_status'] = 126


def run_external_command(command, arguments, set_vars):
    if '/' in command:
        if isfile(command):
            check_and_run_command(command, arguments, set_vars)
        elif isdir(command):
            print('intek-sh: ' + command + ': Is a directory')
            set_vars['exit_status'] = 126
        else:
            print('bash: ' + command + ': No such file or directory')
            set_vars['exit_status'] = 127
    elif 'PATH' in set_vars:
        path = get_command_path(command, set_vars)
        if path:
            check_and_run_command(path, arguments, set_vars)
        else:
            print('intek-sh: ' + command + ': command not found')
            set_vars['exit_status'] = 127
    else:
        print('intek-sh: ' + command + ': command not found')
        set_vars['exit_status'] = 127


def run_command(user_input, set_vars):
    if user_input:
        command, arguments = user_input[0], user_input[1:]
        if command == 'cd':
            change_current_dir(arguments, set_vars)
        elif command == 'printenv':
            print_env_variable(arguments, set_vars)
        elif command == 'export':
            export_variable(arguments, set_vars)
        elif command == 'unset':
            unset_variable(arguments, set_vars)
        elif command == 'exit':
            exit_shell(arguments, set_vars)
        elif command == 'history':
            display_history(arguments, set_vars)
        else:
            run_external_command(command, arguments, set_vars)
