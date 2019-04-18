from signal import signal, SIGHUP
from os import kill


def receive_signal(signum, frame):
    print('\033[1;31mintek-sh$\033[00m ', signum)


def handle_signal():
    signal(SIGHUP, receive_signal)


if __name__ == '__main__':
    handle_signal()
