from readline import set_completer, parse_and_bind


def auto_complete():
    set_completer()
    parse_and_bind('tab: complete')
