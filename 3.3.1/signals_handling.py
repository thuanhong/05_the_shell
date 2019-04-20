from signal import signal, SIGINT, SIGQUIT, SIGTERM


def recieve_signal(signum, frame):
    set_variables['exit_status'] = signum + 128


def control_signal():
    signal(SIGINT, recieve_signal)
    signal(SIGQUIT, recieve_signal)
    signal(SIGTERM, recieve_signal)
