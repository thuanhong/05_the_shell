from signal import signal, SIGINT, SIGQUIT, SIGTERM, SIGTSTP


def call_signal(signal, frame):
    """
    Change exit code and do nothing else
    """
    set_variables['exit_status'] = signal + 128
    pass


def call_sigint(signal, frame):
    """
    Change exit code and raise KeyboardInterrupt exception
    """
    set_variables['exit_status'] = signal + 128
    raise KeyboardInterrupt


def control_signal():
    """
    Depend on user's action on keyboard
    Run the corresponding function to handle the signal
    """
    signal(SIGINT, call_sigint)
    signal(SIGQUIT, call_signal)
    signal(SIGTERM, call_signal)
    signal(SIGTSTP, call_signal)
