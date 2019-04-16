def replace_substring(string=None, key_dict=None):
    for key in key_dict:
        string = string.replace(key, key_dict[key])
    return string


def encode_input(user_input):

    user_input = replace_substring(user_input, {"\\\\":"[\\]"})
    list_input = list(user_input)
    index = 0
    while index < len(list_input):
        if (list_input[index] == "\\" and list_input[index-1] != "["):
            list_input.pop(index)
        else:
            index += 1

    encoded_input =	 "".join(list_input)
    return encoded_input

def handle_backslash(user_input):
    user_input = [user_input]
    for index, each_input in enumerate(user_input):
        user_input[index] = encode_input(each_input)

    return user_input

# decode ()
#     user_input = replace_substring(user_input, {"[\\]":"\\\\"})
