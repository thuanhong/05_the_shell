from os import environ
from os.path import dirname, abspath
from history import read_history_file

class Set():
    variables = {'exit_status': 0, 'history': read_history_file(dirname(abspath(__file__)) + '/.history.txt')}
    variables.update(environ.copy())
