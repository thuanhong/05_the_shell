def read_input():
    raw_input = input('\033[1;31mintek-sh$\033[00m ')
    print('read:', [raw_input])
    return raw_input


def handle_input(raw_input):
    # 1:
    user_input = raw_input.split()
    print('handle 1:', user_input)

    # 2:
    if user_input and user_input[0] in ['cd', 'printenv', 'export',
                                        'unset', 'history', 'exit']:
        user_input[0] = './' + user_input[0] + '.py'
    print('handle 2:', user_input)

    return user_input
