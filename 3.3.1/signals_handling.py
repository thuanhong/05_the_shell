from signal import signal, SIGINT, SIGQUIT, SIGTERM, SIGTSTP


def call_signal(signal, frame):
    set_variables['exit_status'] = signal + 128
    pass

def call_sigint(signal, frame):
    set_variables['exit_status'] = signal + 128
    raise KeyboardInterrupt


def control_signal():
    signal(SIGINT, call_sigint)
    signal(SIGQUIT, call_signal)
    signal(SIGTERM, call_signal)
    signal(SIGTSTP, call_signal)