from typing import Union, List
from sklearn.preprocessing import MinMaxScaler
import numpy as np


def check_for_quit(user_input: Union[str, List[str]]) -> None:
    if "q" in user_input:
        quit()


def calculate_overall_performance_score(problem_list: List[float]) -> float:
    assert len(problem_list) > 0, "List of problems is empty"
    scores = [problem.score for problem in problem_list]
    return np.mean(scores)
