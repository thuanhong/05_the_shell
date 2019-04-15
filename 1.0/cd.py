#!/usr/bin/env python3
from sys import argv
from os import chdir, getcwd
from os.path import isfile, isdir
from export import export_variable


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


if __name__ == '__main__':
    change_current_dir(argv[1:])
