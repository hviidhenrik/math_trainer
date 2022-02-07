import numpy as np
import pytest

from math_trainer.problem import Problem


@pytest.mark.parametrize("int_min, int_max", [[1, 5], [0, 10], [5, 500], [-5, 50]])
def test_problem_result(int_min, int_max):
    problem = Problem(int_min=int_min, int_max=int_max, text_or_aloud="text")
    problem.operator = np.add
    problem._select_and_set_numbers()
    assert problem.result == problem.num1 + problem.num2
