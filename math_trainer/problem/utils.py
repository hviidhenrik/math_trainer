import os
from pathlib import Path
from timeit import default_timer as timer

from gtts import gTTS
from playsound import playsound

from math_trainer.config.definitions import AUDIO_FILES_PATH
from math_trainer.problem.problems import (
    AdditionProblem,
    DivisionProblem,
    LogarithmProblem,
    MultiplicationProblem,
    Problem,
    SquareProblem,
    SquareRootProblem,
    SubtractionProblem,
    TimeDifferenceProblem,
)
from math_trainer.utils import check_for_quit


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
            "logarithm": LogarithmProblem,
            "time_difference": TimeDifferenceProblem,
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
            "division": "divideret med",
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
        elif problem_type == "logarithm":
            text = f"Logaritmen af {self.problem.num1}"
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
        invalid_answer_given = True
        is_done_playing = False
        while invalid_answer_given:
            input_answer = input()
            self.problem.time = timer() - self.problem.time
            check_for_quit(input_answer.lower())

            # check the input - if 's' is detected, stop the game loop
            if input_answer.lower().startswith("s"):
                Problem.instance_count -= 1
                is_done_playing = True
                break

            else:
                # try to convert given answer to integer else print message and pose new problem
                try:
                    input_answer = self.problem.check_user_answer_type(input_answer)
                    invalid_answer_given = False
                    self.problem.answer = input_answer
                    self.problem.calculate_performance_score()
                except ValueError:
                    print('Bad input detected - please provide integer numbers or "stop" (s)\n')
        return is_done_playing

    def print_feedback_on_answer(self):
        if self.problem.answer_is_correct:
            print(
                f"Correct - {self.problem.time:.2f} seconds\n" f"Score: {self.problem.score:.0f}\n", end="\n",
            )
        else:
            print(
                f"Incorrect - {self.problem.time:.2f} seconds\n" f"Score: {self.problem.score:.0f}\n", end="\n",
            )
