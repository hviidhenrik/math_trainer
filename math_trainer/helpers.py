import os
from typing import Union, List

import numpy as np
import pandas as pd

from math_trainer.core import Problem
from math_trainer.definitions import *


def check_for_quit(user_input: Union[str, List[str]]) -> None:
    quit_program = False
    if isinstance(user_input, list):
        quit_program = sum([element.lower() in ["q", "quit"] for element in user_input])
    elif isinstance(user_input, str):
        quit_program = user_input.lower() in ["q", "quit"]
    if quit_program:
        quit()


def calculate_overall_performance_score(problem_list: List[Problem]) -> float:
    assert len(problem_list) > 0, "List of problems is empty"
    scores = [problem.score for problem in problem_list]
    return np.mean(scores)


def add_score_column_to_existing_training_files():
    path = "." + training_files_path
    files = [f for f in os.listdir(path) if f.endswith(".csv")]
    for file in files:
        # add score column to the existing training file
        df = pd.read_csv(path + "/" + file)
        error = abs(df.result - df.answer)
        scores = 100 - (1 + error) ** 2 * df.time ** 2
        df["score"] = [max(0, score) for score in scores]

        # change operation column to problem type
        df["problem_type"] = df["operation"].tail(1).squeeze()
        df = df.drop(columns=["operation"])

        # save the updated df to the file
        df.to_csv(path + "/" + file, index=False, header=True)


if __name__ == "__main__":
    # add_score_column_to_existing_training_files()
    pass
