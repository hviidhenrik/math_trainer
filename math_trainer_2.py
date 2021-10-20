from abc import abstractmethod

import numpy as np
import time


class Problem:
    counter = 0

    def __init__(self):
        self.number1 = np.random.randint(low=min_int, high=max_int + 1)  # + 1 because highest integer is exclusive
        self.number2 = np.random.randint(low=min_int, high=max_int + 1)
        self.correct_answer = None
        self.provided_answer = None
        self.provided_answer_is_correct = None
        Problem.counter += 1

    @abstractmethod
    def print_problem(self):
        pass

    def answer_problem_from_input(self):
        provided_answer = input()
        try:
            self.provided_answer = int(provided_answer)
            self.provided_answer_is_correct = self.provided_answer == self.correct_answer
        except ValueError:
            pass
        return provided_answer

    def print_result(self):
        print("Correct\n" if self.provided_answer_is_correct else "Incorrect\n")


class AdditionProblem(Problem):

    def __init__(self):
        super().__init__()
        self.correct_answer = self.number1 + self.number2

    def print_problem(self):
        print(f"----- Problem {Problem.counter}:")
        print(f"{self.number1} + {self.number2} = ", end="")


class MultiplicationProblem(Problem):

    def __init__(self):
        super().__init__()
        self.correct_answer = self.number1 * self.number2

    def print_problem(self):
        print(f"----- Problem {Problem.counter}:")
        print(f"{self.number1} * {self.number2} = ", end="")


if __name__ == "__main__":
    print("------------ Welcome to math trainer -------------")
    print()
    print("Lowest integer: ")
    min_int = int(input())
    print("Highest integer: ")
    max_int = int(input())

    print("Problems incoming:\n")

    results_correct = []
    answer_timings = []

    run_problem_loop = True
    while run_problem_loop:
        new_problem = AdditionProblem()

        new_problem.print_problem()
        start_time = time.time()
        answer = new_problem.answer_problem_from_input()
        end_time = time.time()

        if "s" in answer:
            run_problem_loop = False
            break

        new_problem.print_result()
        results_correct.append(new_problem.provided_answer_is_correct)
        answer_timings.append(np.round(end_time - start_time, 4))

    print(results_correct)
    print(answer_timings)
    print(f"\nAverage response time: {np.mean(answer_timings):.2f}")
    print(f"{np.sum(results_correct)} of {len(results_correct)} correct answers")




