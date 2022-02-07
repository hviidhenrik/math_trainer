from datetime import date

import numpy as np


class Problem:
    instance_count = 0

    def __init__(self, int_min: int, int_max: int, text_or_aloud: str, **kwargs) -> None:
        Problem.instance_count += 1
        self.mode_to_operator_string_mapping = {
            "addition": "+",
            "subtraction": "-",
            "multiplication": "x",
            "division": "/",
            "square": "x",
        }
        self.problem_type = None
        self.text_or_aloud = text_or_aloud
        self.operator = None
        self.answer_type = None
        self.int_min = int_min
        self.int_max = int_max
        self.answer = np.nan  # the user provided answer
        self.answer_is_correct = None
        self.score = None
        self.error = None  # how far off the provided answer is
        self.time = np.nan  # how long it took to answer
        self.date = date.today().strftime("%b-%d-%Y")

    def calculate_performance_score(self, inversion_offset: float = 100) -> None:
        self.answer_is_correct = self.answer == self.result
        self.error = abs(self.result - self.answer)
        score = inversion_offset - (1 + self.error) ** 2 * self.time ** 2
        self.score = max(0, score)

    def _select_and_set_numbers(self) -> None:
        self.num1 = np.random.randint(self.int_min, self.int_max + 1)  # + 1 because max is exclusive in randint
        self.num2 = np.random.randint(self.int_min, self.int_max + 1)
        self.result = np.round(self.operator(self.num1, self.num2), 2)  # the correct result

    def __str__(self) -> str:
        op = self.mode_to_operator_string_mapping[self.problem_type]
        return f"{self.num1} {op} {self.num2}"

    def __repr__(self) -> str:
        op = self.mode_to_operator_string_mapping[self.problem_type]
        return f"{self.num1} {op} {self.num2}"

    def __del__(self) -> None:
        Problem.instance_count -= 1

    def check_user_answer_type(self, user_answer):
        return self.answer_type(user_answer)


class AdditionProblem(Problem):
    def __init__(self, int_min: int, int_max: int, **kwargs) -> None:
        super().__init__(int_min, int_max, **kwargs)
        self.operator = np.add
        self.problem_type = "addition"
        self.answer_type = int
        self._select_and_set_numbers()


class SubtractionProblem(Problem):
    def __init__(self, int_min: int, int_max: int, **kwargs) -> None:
        super().__init__(int_min, int_max, **kwargs)
        self.operator = np.subtract
        self.problem_type = "subtraction"
        self.answer_type = int
        self._select_and_set_numbers()

    def _select_and_set_numbers(self) -> None:
        self.num1 = np.random.randint(self.int_min, self.int_max + 1)  # + 1 because max is exclusive in randint
        self.num2 = np.random.randint(
            self.int_min, self.num1 + 1
        )  # ensure num2 is always less than num1 for subtraction
        self.result = np.round(self.operator(self.num1, self.num2), 2)  # the correct result


class MultiplicationProblem(Problem):
    def __init__(self, int_min: int, int_max: int, **kwargs) -> None:
        super().__init__(int_min, int_max, **kwargs)
        self.operator = np.multiply
        self.problem_type = "multiplication"
        self.answer_type = int
        self._select_and_set_numbers()


class DivisionProblem(Problem):
    def __init__(
        self, int_min: int, int_max: int, significant_digits: int = 1, only_integers: bool = False, **kwargs,
    ) -> None:
        super().__init__(int_min, int_max, **kwargs)
        self.operator = np.divide
        self.problem_type = "division"
        self.answer_type = float
        self.only_integers = only_integers
        self.significant_digits = significant_digits
        self._select_and_set_numbers()

    def _select_and_set_numbers(self) -> None:
        # prevent division by zero
        if self.int_min == 0:
            self.int_min += 1

        num1 = np.random.randint(self.int_min, self.int_max + 1)  # + 1 because max is exclusive in randint
        num2 = np.random.randint(self.int_min, self.int_max + 1)

        if self.only_integers:
            # keep sampling a new number for num2 until the resulting ratio is integer
            result_is_integer = np.divide(num1, num2) % 1 == 0
            if not result_is_integer:
                while not result_is_integer:
                    num2 = np.random.randint(self.int_min, self.int_max + 1)
                    result_is_integer = np.divide(num1, num2) % 1 == 0

        self.num1 = num1
        self.num2 = num2
        self.result = np.round(self.operator(self.num1, self.num2), self.significant_digits)  # the correct result


class SquareProblem(Problem):
    def __init__(self, int_min: int, int_max: int, **kwargs) -> None:
        super().__init__(int_min, int_max, **kwargs)
        self.operator = np.multiply
        self.problem_type = "square"
        self.answer_type = int
        self._select_and_set_numbers()

    def _select_and_set_numbers(self) -> None:
        self.num1 = np.random.randint(self.int_min, self.int_max + 1)  # + 1 because max is exclusive in randint
        self.num2 = self.num1
        self.result = np.round(self.operator(self.num1, self.num2), 2)  # the correct result


class SquareRootProblem(Problem):
    def __init__(self, int_min: int, int_max: int, significant_digits: int = 1, **kwargs) -> None:
        assert int_max >= int_min >= 0, "Minimum for square root problems must be positive or 0"
        super().__init__(int_min, int_max, **kwargs)
        self.operator = np.sqrt
        self.problem_type = "square_root"
        self.answer_type = float
        self.significant_digits = significant_digits
        self._select_and_set_numbers()

    def _select_and_set_numbers(self) -> None:
        self.num1 = np.random.randint(self.int_min, self.int_max + 1)  # + 1 because max is exclusive in randint
        self.num2 = None
        self.result = np.round(self.operator(self.num1), self.significant_digits)  # the correct result

    def __str__(self) -> str:
        return f"sqrt({self.num1})"

    def __repr__(self) -> str:
        return f"sqrt({self.num1})"


class LogarithmProblem(SquareRootProblem):
    def __init__(self, int_min: int, int_max: int, significant_digits: int = 1, **kwargs) -> None:
        assert int_max >= int_min > 0, "Minimum for logarithm problems must be strictly positive"
        super().__init__(int_min, int_max, significant_digits, **kwargs)
        self.operator = np.log
        self.problem_type = "logarithm"
        self.answer_type = float
        self.significant_digits = significant_digits
        self._select_and_set_numbers()

    def _select_and_set_numbers(self) -> None:
        import random

        available_numbers = [k for k in range(self.int_min, self.int_max + 1)]
        # if eulers number, e, is within the selected range, include it as a problem argument
        if self.int_min <= np.exp(1) <= self.int_max:
            available_numbers.append(np.exp(1))
        self.num1 = random.sample(available_numbers, 1)[0]
        self.num2 = None
        self.result = np.round(self.operator(self.num1), self.significant_digits)  # the correct result

    def __str__(self) -> str:
        return f"log({self.num1})"

    def __repr__(self) -> str:
        return f"log({self.num1})"


class TimeDifferenceProblem(Problem):
    def __init__(self, int_min: int = 1, int_max: int = 24, **kwargs) -> None:
        super().__init__(int_min=int_min, int_max=int_max, **kwargs)
        self.min_time_difference = int_min
        self.max_time_difference = int_max
        assert (
            0 < self.min_time_difference < self.max_time_difference < 24
        ), "Time difference must be minimum 1 and max 23 hours"
        self.operator = None
        self.problem_type = "time_difference"
        self.answer_type = int
        self._select_and_set_numbers()

    def _select_and_set_numbers(self) -> None:
        num1 = np.random.randint(0, 23 + 1)  # + 1 because max is exclusive in randint

        # keep sampling a new number for num2 until the resulting ratio is integer
        result_is_in_allowable_range = False
        while not result_is_in_allowable_range:
            num2 = np.random.randint(0, 23 + 1)
            time_diff = abs(num1 - num2) % 24
            result_is_in_allowable_range = self.min_time_difference <= time_diff <= self.max_time_difference

        self.num1 = min((num1, num2))
        self.num2 = max((num1, num2))
        self.result = self.num2 - self.num1 % 24

    def __str__(self) -> str:
        return f"Hours between {self.num1} and {self.num2}"

    def __repr__(self) -> str:
        return f"Hours between {self.num1} and {self.num2}"
