import numpy as np
from datetime import date


class Problem:
    instance_count = 0

    def __init__(self, min: int, max: int, **kwargs) -> None:
        Problem.instance_count += 1
        self.mode_to_operator_string_mapping = {
            "addition": "+",
            "subtraction": "-",
            "multiplication": "x",
            "division": "/",
            "square": "x",
        }
        self.problem_type = None
        self.operator = None
        self.answer_type = None
        self.min = min
        self.max = max
        self.answer = np.nan  # the user provided answer
        self.answer_is_correct = None
        self.score = None
        self.error = None  # how far off the provided answer is
        self.time = np.nan  # how long it took to answer
        self.date = date.today().strftime("%b-%d-%Y")

    def calculate_performance_score(self, inversion_offset: float = 100) -> None:
        self.answer_is_correct = self.answer == self.result
        self.error = abs(self.result - self.answer)
        score = inversion_offset - (1 + self.error)**2 * self.time**2
        self.score = max(0, score)


    def _select_and_set_numbers(self) -> None:
        self.num1 = np.random.randint(
            self.min, self.max + 1
        )  # + 1 because max is exclusive in randint
        self.num2 = np.random.randint(self.min, self.max + 1)
        self.result = np.round(
            self.operator(self.num1, self.num2), 2
        )  # the correct result

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
    def __init__(self, min: int, max: int, **kwargs) -> None:
        super().__init__(min, max)
        self.operator = np.add
        self.problem_type = "addition"
        self.answer_type = int
        self._select_and_set_numbers()


class SubtractionProblem(Problem):
    def __init__(self, min: int, max: int, **kwargs) -> None:
        super().__init__(min, max)
        self.operator = np.subtract
        self.problem_type = "subtraction"
        self.answer_type = int
        self._select_and_set_numbers()

    def _select_and_set_numbers(self) -> None:
        self.num1 = np.random.randint(
            self.min, self.max + 1
        )  # + 1 because max is exclusive in randint
        self.num2 = np.random.randint(
            self.min, self.num1 + 1
        )  # ensure num2 is always less than num1 for subtraction
        self.result = np.round(
            self.operator(self.num1, self.num2), 2
        )  # the correct result


class MultiplicationProblem(Problem):
    def __init__(self, min: int, max: int, **kwargs) -> None:
        super().__init__(min, max)
        self.operator = np.multiply
        self.problem_type = "multiplication"
        self.answer_type = int
        self._select_and_set_numbers()


class DivisionProblem(Problem):
    def __init__(
            self,
            min: int,
            max: int,
            significant_digits: int = 1,
            only_integers: bool = False,
            **kwargs,
    ) -> None:
        super().__init__(min, max)
        self.operator = np.divide
        self.problem_type = "division"
        self.answer_type = float
        self.only_integers = only_integers
        self.significant_digits = significant_digits
        self._select_and_set_numbers()

    def _select_and_set_numbers(self) -> None:
        # prevent division by zero
        if self.min == 0:
            self.min += 1

        num1 = np.random.randint(
            self.min, self.max + 1
        )  # + 1 because max is exclusive in randint
        num2 = np.random.randint(self.min, self.max + 1)

        if self.only_integers:
            # keep sampling a new number for num2 until the resulting ratio is integer
            result_is_integer = np.divide(num1, num2) % 1 == 0
            if not result_is_integer:
                while not result_is_integer:
                    num2 = np.random.randint(self.min, self.max + 1)
                    result_is_integer = np.divide(num1, num2) % 1 == 0

        self.num1 = num1
        self.num2 = num2
        self.result = np.round(
            self.operator(self.num1, self.num2), self.significant_digits
        )  # the correct result


class SquareProblem(Problem):
    def __init__(self, min: int, max: int, **kwargs) -> None:
        super().__init__(min, max)
        self.operator = np.multiply
        self.problem_type = "square"
        self.answer_type = int
        self._select_and_set_numbers()

    def _select_and_set_numbers(self) -> None:
        self.num1 = np.random.randint(
            self.min, self.max + 1
        )  # + 1 because max is exclusive in randint
        self.num2 = self.num1
        self.result = np.round(
            self.operator(self.num1, self.num2), 2
        )  # the correct result


class SquareRootProblem(Problem):
    def __init__(self, min: int, max: int, significant_digits: int = 1, **kwargs) -> None:
        assert max >= min >= 0, "Minimum for square root problems must be positive or 0"
        super().__init__(min, max)
        self.operator = np.sqrt
        self.problem_type = "square_root"
        self.answer_type = float
        self.significant_digits = significant_digits
        self._select_and_set_numbers()

    def _select_and_set_numbers(self) -> None:
        self.num1 = np.random.randint(
            self.min, self.max + 1
        )  # + 1 because max is exclusive in randint
        self.num2 = None
        self.result = np.round(
            self.operator(self.num1), self.significant_digits
        )  # the correct result

    def __str__(self) -> str:
        return f"sqrt({self.num1})"

    def __repr__(self) -> str:
        return f"sqrt({self.num1})"
