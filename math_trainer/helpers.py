# helper function to take validate and take integer input from the user
from typing import Union, List


def input_number(message, exception_message=None):
    # if no exception message is provided, use a standard one
    if exception_message is None:
        exception_message = "Bad input detected. Please provide an integer"
    # loop to check for and obtain proper integer input
    while True:
        user_input = input(message)
        try:
            user_input = int(user_input)
        except ValueError:
            print(exception_message)
            continue
        else:
            break
    return user_input


def check_for_quit(user_input: Union[str, List[str]]):
    if "q" in user_input:
        quit()
