def encode_backslash(user_input):
    """
    Turn double backslash into
    a single backslash inside squares
    """
    return user_input.replace("\\\\", "[\\]")


def decode_backslash(user_input):
    """
    Turn a single backslash inside squares
    into a single backslash
    """
    user_input.replace("[\\]", "\\")
    return user_input.replace("[\\]", "\\")


def remove_backslash(user_input):
    """
    Remove all backslash that is used to escaped another character
    """
    list_string = list(user_input)
    index = 0
    # check if it is an decoded backslash or not
    # if false, remove it
    while index < len(list_string):
        if list_string[index] == "\\" and list_string[index - 1] != "[":
            list_string.pop(index)
        else:
            index += 1
    return "".join(list_string)
