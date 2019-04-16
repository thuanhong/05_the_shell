from os import environ, chdir, getcwd
from os.path import exists, isfile, isdir, join
from subprocess import run


def check_and_move_dir(path):
    if isdir(path):
        chdir(path)
        export_variable(['PWD=' + getcwd()])
    elif isfile(path):
        print('intek-sh: cd: ' + path + ': Not a directory')
    else:
        print('intek-sh: cd: ' + path + ': No such file or directory')


def change_current_dir(arguments):
    if arguments:
        check_and_move_dir(arguments[0])
    else:
        if 'HOME' in environ:
            check_and_move_dir(environ['HOME'])
        else:
            print('intek-sh: cd: HOME not set')


def print_env_variable(arguments):
    if arguments:
        for arg in arguments:
            if arg in environ:
                print(environ[arg])
    else:
        for key, value in environ.items():
            print(key + '=' + value)


def export_variable(arguments):
    if arguments:
        for arg in arguments:
            if arg[0].isnumeric() or arg.startswith('='):
                print("intek-sh: export: `" + arg +
                      "': not a valid identifier")
            elif '=' in arg:
                pos = arg.find('=')
                environ[arg[:pos]] = arg[pos + 1:]
    else:
        for key, value in sorted(environ.items()):
            print('export ' + key + '=' + value)


def unset_variable(arguments):
    for arg in arguments:
        if arg[0].isnumeric() or arg.startswith('='):
            print("intek-sh: unset: `" + arg + "': not a valid identifier")
        elif arg in environ:
            del environ[arg]


def exit_shell(arguments):
    if arguments:
        pass
    else:
        exit()


def display_history(arguments):
    pass


def get_command_path(command):
    for path in environ['PATH'].split(':'):
        command_path = join(path, command)
        if exists(command_path):
            return command_path


def check_and_run_command(command, arguments):
    try:
        run([command] + arguments)
    except PermissionError:
        print('intek-sh: ' + command + ': Permission denied')


def run_external_command(command, arguments):
    if '/' in command:
        if isfile(command):
            check_and_run_command(command, arguments)
        elif isdir(command):
            print('intek-sh: ' + command + ': Is a directory')
        else:
            print('bash: ' + command + ': No such file or directory')
    elif 'PATH' in environ:
        path = get_command_path(command)
        if path:
            check_and_run_command(path, arguments)
        else:
            print('intek-sh: ' + command + ': command not found')
    else:
        print('intek-sh: ' + command + ': command not found')
