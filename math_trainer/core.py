"""
TO DO:
    - implement time difference mode, e.g. hours between 22 and 8
    - add option to cancel choice in input, e.g. if saving to a file, cancel it
        if "cancel" or "stop" is detected as file name
    - improve integer division mode to give actually non-trivial problems that arent
        a/1 or a/a - prevent prime numbers
    - make square root estimation mode
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
from timeit import default_timer as timer


# define a problem class
# TODO: refactor so Problem becomes a super class for sub problems (AdditionProblem, MultiplicationProblem etc.)
class Problem:
    instance_count = 0

    def __init__(self, min: int, max: int, **kwargs):
        Problem.instance_count += 1
        self.mode_to_operator_string_mapping = {"addition": "+", "multiplication": "x",
                                                "division": "/", "square": "x"}
        self.problem_type = None
        self.operator = None
        self.answer_type = None
        self.min = min
        self.max = max
        self.answer = np.nan  # the user provided answer
        self.error = np.nan  # how far off the provided answer is
        self.time = np.nan  # how long it took to answer
        self.date = date.today().strftime("%b-%d-%Y")

    def _select_and_set_numbers(self):
        self.num1 = np.random.randint(self.min, self.max + 1)  # + 1 because max is exclusive in randint
        self.num2 = np.random.randint(self.min, self.max + 1)
        self.result = np.round(self.operator(self.num1, self.num2), 2)  # the correct result

    def __str__(self):
        op = self.mode_to_operator_string_mapping[self.problem_type]
        return f"{self.num1} {op} {self.num2}"

    def __repr__(self):
        op = self.mode_to_operator_string_mapping[self.problem_type]
        return f"{self.num1} {op} {self.num2}"

    def __del__(self):
        Problem.instance_count -= 1

    def check_user_answer_type(self, user_answer):
        return self.answer_type(user_answer)


class AdditionProblem(Problem):
    def __init__(self, min: int, max: int, **kwargs):
        super().__init__(min, max)
        self.operator = np.add
        self.problem_type = "addition"
        self.answer_type = int
        self._select_and_set_numbers()


class MultiplicationProblem(Problem):
    def __init__(self, min: int, max: int, **kwargs):
        super().__init__(min, max)
        self.operator = np.multiply
        self.problem_type = "multiplication"
        self.answer_type = int
        self._select_and_set_numbers()


class IntegerDivisionProblem(Problem):
    def __init__(self, min: int, max: int, **kwargs):
        super().__init__(min, max)
        self.operator = np.divide
        self.problem_type = "division"
        self.answer_type = int
        self._select_and_set_numbers()

    def _select_and_set_numbers(self):
        # prevent division by zero
        if self.min == 0:
            self.min += 1

        num1 = np.random.randint(self.min, self.max + 1)  # + 1 because max is exclusive in randint
        num2 = np.random.randint(self.min, self.max + 1)

        # keep sampling a new number for num2 until the resulting ratio is integer
        result_is_integer = np.divide(num1, num2) % 1 != 0
        if not result_is_integer:
            while not result_is_integer:
                num2 = np.random.randint(self.min, self.max + 1)
                result_is_integer = np.divide(num1, num2) % 1 != 0

        self.num1 = num1
        self.num2 = num2
        self.result = np.round(self.operator(self.num1, self.num2), 2)  # the correct result


class SquareProblem(Problem):
    def __init__(self, min: int, max: int, **kwargs):
        super().__init__(min, max)
        self.operator = np.multiply
        self.problem_type = "square"
        self.answer_type = int
        self._select_and_set_numbers()

    def _select_and_set_numbers(self):
        self.num1 = np.random.randint(self.min, self.max + 1)  # + 1 because max is exclusive in randint
        self.num2 = self.num1
        self.result = np.round(self.operator(self.num1, self.num2), 2)  # the correct result


class SquareRootProblem(Problem):
    def __init__(self, min: int, max: int, significant_digits: int = 1, **kwargs):
        assert max >= min >= 0, "Minimum for square root problems must be positive or 0"
        super().__init__(min, max)
        self.operator = np.sqrt
        self.problem_type = "square_root"
        self.answer_type = float
        self.significant_digits = significant_digits
        self._select_and_set_numbers()

    def _select_and_set_numbers(self):
        self.num1 = np.random.randint(self.min, self.max + 1)  # + 1 because max is exclusive in randint
        self.num2 = None
        self.result = np.round(self.operator(self.num1), self.significant_digits)  # the correct result

    def __str__(self):
        return f"sqrt({self.num1})"

    def __repr__(self):
        return f"sqrt({self.num1})"


if __name__ == "__main__":
    problem = IntegerDivisionProblem(2, 4, "division")
