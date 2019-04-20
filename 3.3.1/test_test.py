#!/usr/bin/env python3


def check_nearest(pos, pos_list):
    num_list = [i for i in pos_list if i != -1]
    if num_list:
        return pos < min(num_list)
    return not pos == -1


def split_logical_operator(user_input):
    new_input = []
    if user_input:
        a = user_input.find('&&')
        b = user_input.find('||')
        c = user_input.find('(')
        d = user_input.rfind(')')
        print(user_input)
        print(a, b, c, d)

        if check_nearest(a, [b, c]):
            new_input.append(user_input[:a])
            new_input.append('&&')
            new_input += split_logical_operator(user_input[a + 2:])
        elif check_nearest(b, [a, c]):
            new_input.append(user_input[:b])
            new_input.append('||')
            new_input += split_logical_operator(user_input[b + 2:])
        elif check_nearest(c, [a, b]):
            new_input.append(user_input[c:d + 1])
            new_input += split_logical_operator(user_input[d + 1:])
        else:
            new_input.append(user_input)
    return new_input


if __name__ == '__main__':
    user_input = ['((A)&&B&&(((A)&&C)&&(D||E)))&&F',
                  '(A)&&B&&(((A)&&C)&&(D||E))',
                  'A',
                  '((A)&&C)&&(D||E)',
                  '(A)&&C',
                  'D||E',
                  'A']
    for item in user_input[1:2]:
        item = split_logical_operator(item)
        item = [i.strip() for i in item if i.strip()]
        print(item)
