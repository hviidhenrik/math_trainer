from math_trainer.core import *
from math_trainer.helpers import input_number

import os
import numpy as np
from timeit import default_timer as timer
import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

# prompt the user whether to quick start or use existing/new file and check input


print("WELCOME TO MATH TRAINER v1.0")
print("----------------------------")
print("How would you like to play?\n")

# print("Quick start (q) or save results to existing/new file (e)?\n")

# start = input("Quick start (q) or save results to existing/new file (e)?\n")
while True:
    print("[1] Quick start")
    print("[2] Create/select a file to save to")
    quick_start_or_with_save_file = input("Your choice: ")
    print("----------------------------\n")

    # check the input for validity

    ##
    start_modes = {"1": "quick", "2": "savefile", "q": "quit"}
    print()
    # validate input and prompt user again if erroneous input was detected
    try:
        quick_start_or_with_save_file = start_modes[quick_start_or_with_save_file]
    except KeyError:
        print("Bad input detected. Must be either 1 or 2\n")
    # hidden quit option (mostly for my own testing purposes)
    else:
        if quick_start_or_with_save_file == "quit":
            raise SystemExit
        else:
            break

# if existing/new file was chosen, let user decide the file to save to
if quick_start_or_with_save_file == "savefile":
    # print an overview of already existing csv files in directory
    print("\nThe following data files were found already:\n")
    while True:
        files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(".csv")]
        [print("[", idx + 1, "] ", f, sep="") for idx, f in enumerate(files)]

        # prompt the user for a desired file
        file = input("Write the name or number of the file you wish to use:\n")

        # check the given input and convert to integer if a number was given
        try:
            file = int(file)
        # exception raised if it is a string input
        except ValueError:
            # if input is empty ask user to provide a better filename
            if all(i == " " for i in file):
                print("\nEmpty input detected. Please provide a filename or number\n")
                continue
            # if filename isnt empty, check for or append .csv to it
            file = file if file.endswith(".csv") else file + ".csv"
            # check if the file exists to determine the inclusion of a header in csv
            file_exists = file in files
            break
        # if integer input
        else:
            idx = file - 1
            file = files[idx]
            file_exists = True
            break

# %% main section that runs the practice loop

# initiate counts, lists and integer limits
count = 0
corrects = 0
problem_array = []

# get desired math operation using input and a predefined dictionary of operations
while True:
    print("[1] Addition")
    print("[2] Multiplication")
    print("[3] Division")
    print("[4] Square")

    problem_type = input("Your choice: ")
    print("----------------------------\n")

    mode_mapping = {"1": "addition", "2": "multiplication", "3": "division", "4": "square"}

    # validate input and prompt user again if erroneous input was detected
    try:
        problem_type = mode_mapping[problem_type]
    except KeyError:
        print("Bad input detected. Must be either 1, 2 or 3 as below: \n")
        continue
    else:
        break

# get upper and lower limits of the math problems to be posed
while True:
    int_min = input("Lowest possible integer: ")
    int_max = input("Highest possible integer: ")
    print("")

    # check that the provided limits are actually integers, else prompt for it again
    try:
        int_min, int_max = [int(limit) for limit in [int_min, int_max]]
    except ValueError:
        print("Bad input detected. The limits must be integer numbers")
        continue
    else:
        break

# run the problem generating loop
while True:
    if count % 10 == 9 or count == 0:
        print(f"--- Problem {count + 1} -------------", end="")
    else:
        print("----------------------------", end="")

    # initiate a problem instance
    mode_to_problem_type_mapping = {"addition": AdditionProblem, "multiplication": MultiplicationProblem,
                                    "division": IntegerDivisionProblem, "square": SquareProblem}
    problem = mode_to_problem_type_mapping[problem_type](min=int_min, max=int_max)

    # start timer
    timer_start = timer()

    # the answer from the user
    input_answer = input(f"{problem} = ")

    # check the input - if 's' is detected, stop the loop
    if input_answer.lower().startswith("s"):
        timer_end = timer()
        del problem
        break
    # else try to convert the input to integer
    else:
        # try to convert given answer to integer else print message and pose new problem
        try:
            input_answer = int(input_answer)
        except ValueError:
            print("Bad input detected - please provide integer numbers or \"stop\" (s)")
            print("")
            del problem
            continue

            # if provided answer is correct
        if problem.result == input_answer:
            print("Correct\n", end="\n")
            corrects += 1
        # if it's not correct
        else:
            print("Incorrect\n", end="\n")

    # store timing, problem and answer and increment problem count
    timer_end = timer()
    problem.time = timer_end - timer_start
    count += 1
    problem_array.append(problem)
    problem.answer = input_answer

# compute and print mean response time
if len(problem_array) > 0:
    mean_time = np.mean([prob.time for prob in problem_array])
    print("\n-------------------------------------------", end="\n")
    print("----------------- RESULTS -----------------", end="\n")
    print("-------------------------------------------\n", end="\n")
    print("{}% correct ({} out of {})".format(np.round(100 * corrects / count, 2), corrects, count))
    print("Average response time: ", np.round(np.mean(mean_time), 2), "seconds")

    # turn into a dataset
    df = pd.DataFrame({"time": [prob.time for prob in problem_array],
                       "num1": [prob.num1 for prob in problem_array],
                       "num2": [prob.num2 for prob in problem_array],
                       "result": [prob.result for prob in problem_array],
                       "answer": [prob.answer for prob in problem_array],
                       "date": [prob.date for prob in problem_array]})
    df["correct"] = [1 if diff == 0 else 0 for diff in df.answer - df.result]  # codes it as binary integers
    df["operation"] = problem_type
else:
    quit()

# if quick start was chosen in the beginning prompt for saving
if quick_start_or_with_save_file == "quick" and len(problem_array) > 0:
    # print results
    df_to_print = pd.DataFrame({"mean": np.mean(df["time"]),
                                "median": np.median(df["time"]),
                                "std": np.std(df["time"])},
                               index=[0])
    print("\nResponse time (seconds):\n", df_to_print.round(3))
    # ask if user wishes to save results to a file
    input_savefile = input("Save your results to a file? [y/n]\n")

    # if yes, print list of already existing csv files in directory to save to
    if input_savefile.lower().startswith("y"):
        # print an overview of already existing csv files in directory
        print("----------------------------------------")
        print("The following data files were found already:\n")
        while True:
            files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(".csv")]
            [print(idx + 1, f) for idx, f in enumerate(files)]

            # prompt the user for a desired file
            file = input("Write the name or number of the file you wish to use:\n")
            # check the given input and convert to integer if a number was given
            try:
                file = int(file)
            # exception raised if it is a string input
            except ValueError:
                # if input is empty ask user to provide a better filename
                if all(i == " " for i in file):
                    print("\nEmpty input detected. Please provide a filename or number\n")
                    continue
                file = file if file.endswith(".csv") else file + ".csv"
                break
            # if integer input
            else:
                idx = file - 1
                file = files[idx]
                break

        write_mode = "a" if file in files else "w"  # append or write
        df.to_csv(file, index=False, mode=write_mode, header=write_mode == "w")
    else:
        quit()

# else simply save to the file specified in the beginning
elif quick_start_or_with_save_file == "savefile" and len(problem_array) > 0:
    df.to_csv(file, index=False, mode="a", header=not file_exists)

df1 = pd.read_csv(file)
print("")
print(df1)

# mean and standard deviation analysis of response times
dates = df1.date.unique()
date_arrays = [df1[df1["date"] == date][["time", "date"]] for date in dates]

# print mean and sd
df5 = pd.DataFrame([(np.mean(dates.time),
                     np.median(dates.time),
                     np.std(dates.time),
                     dates.date.unique()) for dates in date_arrays],
                   columns=["mean", "median", "sd", "date"])
print(df5)

# perform t-test with unequal variances
first = date_arrays[0].time
last = date_arrays[-1].time

stats.ttest_ind(first, last, equal_var=False)

# plot timing distributions
sns.set(color_codes=True)
sns.kdeplot(first, label="First")
sns.kdeplot(last, label="Latest")
plt.legend()
plt.title("Timing distributions")
plt.xlabel("Seconds")
plt.ylabel("Frequency")
plt.show()
