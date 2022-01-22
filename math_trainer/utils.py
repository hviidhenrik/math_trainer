import os
from typing import Any, List, Union

import numpy as np
import pandas as pd
from numpy import ndarray

from config.definitions import *


def check_for_quit(user_input: Union[str, List[str]]) -> None:
    quit_program = False
    if isinstance(user_input, list):
        quit_program = sum([element.lower() in ["q", "quit"] for element in user_input])
    elif isinstance(user_input, str):
        quit_program = user_input.lower() in ["q", "quit"]
    if quit_program:
        quit()


def calculate_overall_performance_score(problem_list: List[Any]) -> ndarray:
    assert len(problem_list) > 0, "List of problems is empty"
    scores = [problem.score for problem in problem_list]
    return np.mean(scores)


def add_text_or_aloud_column_to_existing_training_files():
    path = TRAINING_FILES_PATH
    files = [f for f in os.listdir(path) if f.endswith(".csv")]
    for file in files:
        # add score column to the existing training file
        df = pd.read_csv(path / file)
        df["text_or_aloud"] = "text"

        # save the updated df to the file
        df.to_csv(path / file, index=False, header=True)


if __name__ == "__main__":
    add_text_or_aloud_column_to_existing_training_files()
