import os
from datetime import date
from timeit import default_timer as timer

import numpy as np
from gtts import gTTS
from playsound import playsound

from config.definitions import *
from math_trainer.helpers import check_for_quit


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
        self.num1 = np.random.randint(
            self.int_min, self.int_max + 1
        )  # + 1 because max is exclusive in randint
        self.num2 = np.random.randint(self.int_min, self.int_max + 1)
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
        self.num1 = np.random.randint(
            self.int_min, self.int_max + 1
        )  # + 1 because max is exclusive in randint
        self.num2 = np.random.randint(
            self.int_min, self.num1 + 1
        )  # ensure num2 is always less than num1 for subtraction
        self.result = np.round(
            self.operator(self.num1, self.num2), 2
        )  # the correct result


class MultiplicationProblem(Problem):
    def __init__(self, int_min: int, int_max: int, **kwargs) -> None:
        super().__init__(int_min, int_max, **kwargs)
        self.operator = np.multiply
        self.problem_type = "multiplication"
        self.answer_type = int
        self._select_and_set_numbers()


class DivisionProblem(Problem):
    def __init__(
            self,
            int_min: int,
            int_max: int,
            significant_digits: int = 1,
            only_integers: bool = False,
            **kwargs,
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

        num1 = np.random.randint(
            self.int_min, self.int_max + 1
        )  # + 1 because max is exclusive in randint
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
        self.result = np.round(
            self.operator(self.num1, self.num2), self.significant_digits
        )  # the correct result


class SquareProblem(Problem):
    def __init__(self, int_min: int, int_max: int, **kwargs) -> None:
        super().__init__(int_min, int_max, **kwargs)
        self.operator = np.multiply
        self.problem_type = "square"
        self.answer_type = int
        self._select_and_set_numbers()

    def _select_and_set_numbers(self) -> None:
        self.num1 = np.random.randint(
            self.int_min, self.int_max + 1
        )  # + 1 because max is exclusive in randint
        self.num2 = self.num1
        self.result = np.round(
            self.operator(self.num1, self.num2), 2
        )  # the correct result


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
        self.num1 = np.random.randint(
            self.int_min, self.int_max + 1
        )  # + 1 because max is exclusive in randint
        self.num2 = None
        self.result = np.round(
            self.operator(self.num1), self.significant_digits
        )  # the correct result

    def __str__(self) -> str:
        return f"sqrt({self.num1})"

    def __repr__(self) -> str:
        return f"sqrt({self.num1})"


class TimeDifferenceProblem(Problem):
    def __init__(self, int_min: int = 1, int_max: int = 24, **kwargs) -> None:
        super().__init__(int_min=int_min,
                         int_max=int_max, **kwargs)
        self.min_time_difference = int_min
        self.max_time_difference = int_max
        assert 0 < self.min_time_difference < self.max_time_difference < 24, "Time difference must be minimum 1 and max 23 hours"
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


class ProblemGenerator:
    def __init__(self, problem_type: str, **kwargs) -> None:
        self.problem_type = problem_type
        self.problem_type_to_problem_object_mapping = {
            "addition": AdditionProblem,
            "subtraction": SubtractionProblem,
            "multiplication": MultiplicationProblem,
            "division": DivisionProblem,
            "square": SquareProblem,
            "square_root": SquareRootProblem,
            "time_difference": TimeDifferenceProblem
        }
        self.problem_arguments = kwargs

    def generate_problem(self):
        # generate a problem based on the selected problem type and other choices
        return self.problem_type_to_problem_object_mapping[self.problem_type](**self.problem_arguments)


class ProblemReader:
    def __init__(self, problem: Problem, path: Path):
        self.problem_path = path / "temp_problem.mp3"
        if not "audio_files" in os.listdir():
            os.mkdir("audio_files")
        self.problem = problem
        self.operator_string_to_speech_mapping = {
            "addition": "plus",
            "subtraction": "minus",
            "multiplication": "gange",
            "division": "divideret med"
        }
        self.problem_text_to_be_read = self._format_string_for_speech()
        tts = gTTS(self.problem_text_to_be_read, lang="da")
        tts.save(str(self.problem_path))

    def read_problem_aloud(self):
        playsound(str(self.problem_path))
        os.remove(self.problem_path)

    def _format_string_for_speech(self):
        problem_type = self.problem.problem_type
        if problem_type == "square":
            text = f"{self.problem.num1} i anden"
        elif problem_type == "square_root":
            text = f"Kvadratroden af {self.problem.num1}"
        elif problem_type == "time_difference":
            text = f"Timer mellem {self.problem.num1} og {self.problem.num2}"
        else:
            text = f"{self.problem.num1} {self.operator_string_to_speech_mapping[problem_type]} {self.problem.num2}"
        return text


class ProblemIO:
    def __init__(self, problem: Problem):
        self.problem = problem
        pass

    def print_problem(self):
        if self.problem.text_or_aloud == "aloud":
            ProblemReader(self.problem, AUDIO_FILES_PATH).read_problem_aloud()
            print(f"\nAnswer: ", end="")
        else:
            print(f"{self.problem} = ", end="")
        self.problem.time = timer()

    def take_problem_answer_as_input(self):
        input_answer = input()
        self.problem.time = timer() - self.problem.time
        check_for_quit(input_answer.lower())

        # check the input - if 's' is detected, stop the game loop
        is_done_playing = False
        if input_answer.lower().startswith("s"):
            Problem.instance_count -= 1
            is_done_playing = True

        else:
            # try to convert given answer to integer else print message and pose new problem
            try:
                input_answer = self.problem.check_user_answer_type(input_answer)
            except ValueError:
                print("Bad input detected - please provide integer numbers or \"stop\" (s)\n")
                Problem.instance_count -= 1

            # TODO fix exit bug here if empty input
            self.problem.answer = input_answer
            self.problem.calculate_performance_score()
        return is_done_playing

    def print_feedback_on_answer(self):
        if self.problem.answer_is_correct:
            print(f"Correct - {self.problem.time:.2f} seconds\n"
                  f"Score: {self.problem.score:.0f}\n", end="\n")
        else:
            print(f"Incorrect - {self.problem.time:.2f} seconds\n"
                  f"Score: {self.problem.score:.0f}\n", end="\n")
