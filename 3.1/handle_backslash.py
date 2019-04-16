def encode_backslash(user_input):
    return user_input.replace("\\\\", "[\\]")
    

def decode_backslash(user_input):
    user_input.replace("[\\]", "\\")
    return user_input.replace("[\\]", "\\")


def remove_backslash(user_input):
    list_string = list(user_input)
    index = 0 
    while index < len(list_string):
        if list_string[index] == "\\" and list_string[index - 1] != "[":
            list_string.pop(index)
        else:
            index += 1

    return "".join(list_string)
