"""
TO DO:
    - implement time difference mode, e.g. hours between 22 and 8
    - add option to cancel choice in input, e.g. if saving to a file, cancel it
        if "cancel" or "stop" is detected as file name
    - improve integer division mode to give actually non-trivial problems that arent
        a/1 or a/a - prevent prime numbers
    - implement a true division mode where results can be rounded fractions, e.g. 0.33
    - make graphical interface
    - catch empty input when selecting file to save
    - ensure that results can only be saved to files with the same game mode,
       e.g. addition, multiplication etc) to avoid data getting mixed up -
       alternatively, add a column in the data that shows the operation for
       each problem/row
    - add option to "go back" when selecting game mode, whether to save and such
    - add hidden "quit option" to all input prompts
"""

import numpy as np
from datetime import date


# define a problem class
class Problem:
    instance_count = 0

    def __init__(self, min: int, max: int, mode: str):
        Problem.instance_count += 1
        mode_to_operator_function_mapping = {"addition": np.add, "multiplication": np.multiply,
                                             "division": np.divide, "square": np.multiply}
        self.mode_to_operator_string_mapping = {"addition": "+", "multiplication": "x",
                                                "division": "/", "square": "x"}
        self.min = min
        self.max = max
        self.mode = mode
        self.operator = mode_to_operator_function_mapping[mode.lower()]  # should be a function such as np.add
        self.answer = np.nan  # the user provided answer
        self.error = np.nan  # how far off the provided answer is
        self.time = np.nan  # how long it took to answer
        self.date = date.today().strftime("%b-%d-%Y")
        self._select_and_set_numbers()

    def _select_and_set_numbers(self):
        # prevent division by zero
        if self.mode == "division" and self.min == 0:
            self.min += 1

        num1 = np.random.randint(self.min, self.max + 1)  # + 1 because max is exclusive in randint
        num2 = np.random.randint(self.min, self.max + 1)

        # keep sampling a new number for num2 until the resulting ratio is integer
        result_is_integer = np.divide(num1, num2) % 1 != 0
        if self.mode == "division" and not result_is_integer:
            while not result_is_integer:
                num2 = np.random.randint(self.min, self.max + 1)
                result_is_integer = np.divide(num1, num2) % 1 != 0
        elif self.mode == "square":
            num2 = num1

        self.num1 = num1
        self.num2 = num2
        self.result = np.round(self.operator(self.num1, self.num2), 2)  # the correct result

    def __str__(self):
        op = self.mode_to_operator_string_mapping[self.mode]
        return f"{self.num1} {op} {self.num2}"

    def __repr__(self):
        op = self.mode_to_operator_string_mapping[self.mode]
        return f"{self.num1} {op} {self.num2}"

    def __del__(self):
        Problem.instance_count -= 1