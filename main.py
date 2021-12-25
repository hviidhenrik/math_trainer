import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats

from math_trainer.core import *
from math_trainer.helpers import check_for_quit, calculate_overall_performance_score

print("WELCOME TO MATH TRAINER v1.2")
print("----------------------------")
print("How would you like to play?\n")

while True:
    print("[1] Quick start")
    print("[2] Create/select a file to save to")
    quick_start_or_with_save_file = input("Your choice: ")
    check_for_quit(quick_start_or_with_save_file.lower())
    print("----------------------------\n")

    start_modes = {"1": "quick", "2": "savefile"}
    print()
    # validate input and prompt user again if erroneous input was detected
    try:
        quick_start_or_with_save_file = start_modes[quick_start_or_with_save_file]
    except KeyError:
        print("Bad input detected. Must be either 1 or 2\n")
    else:
        break

# if existing/new file was chosen, let user decide the file to save to
if quick_start_or_with_save_file == "savefile":
    # print an overview of already existing csv files in directory
    print("\nThe following data files were found already:\n")
    while True:
        files = [f for f in os.listdir(TRAINING_FILES_PATH) if f.endswith(".csv")]
        [print("[", idx + 1, "] ", f, sep="") for idx, f in enumerate(files)]

        # prompt the user for a desired file
        file = input("Write the name or number of the file you wish to use:\n")
        check_for_quit(file.lower())

        # check the given input and convert to integer if a number was given
        try:
            file = int(file)
        # exception raised if it is a string input
        except ValueError:
            # if input is empty ask user to provide a better filename
            if all(i == " " for i in file):
                print("\nEmpty input detected. Please provide a filename or number\n")
                continue
            # if filename isn't empty, check for or append .csv to it
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

# get desired math operation using input and a predefined dictionary of operations
while True:
    print("----- Game mode: as text or read aloud -----")
    print("[1] Text")
    print("[2] Read aloud")

    game_mode_as_text_or_aloud = input("Your choice: ")
    check_for_quit(game_mode_as_text_or_aloud.lower())

    print("----------------------------\n")

    # validate input and prompt user again if erroneous input was detected
    try:
        game_mode_as_text_or_aloud = (
            "text" if int(game_mode_as_text_or_aloud) == 1 else "aloud"
        )
    except (KeyError, ValueError):
        print("Bad input detected. Must be either 1 or 2: \n")
        continue
    else:
        break

# get desired math operation using input and a predefined dictionary of operations
while True:
    print("----- Problem type -----")
    print("[1] Addition")
    print("[2] Subtraction")
    print("[3] Multiplication")
    print("[4] Division")
    print("[5] Square")
    print("[6] Square root approximation")
    print("[7] Natural Logarithm approximation")
    print("[8] Time difference in hours")

    selected_problem_type = input("Your choice: ")
    check_for_quit(selected_problem_type.lower())

    print("----------------------------\n")

    input_to_problem_type_mapping = {
        "1": "addition",
        "2": "subtraction",
        "3": "multiplication",
        "4": "division",
        "5": "square",
        "6": "square_root",
        "7": "logarithm",
        "8": "time_difference",
    }

    # validate input and prompt user again if erroneous input was detected
    try:
        selected_problem_type = input_to_problem_type_mapping[selected_problem_type]
    except KeyError:
        print("Bad input detected. Must be either 1, 2, 3, 4, 5, 6, 7 or 8 as below: \n")
        continue
    else:
        break

# get upper and lower limits of the math problems to be posed
while True:
    print("----- Problem limits -----")
    if selected_problem_type == "time_difference":
        int_min = input("Lowest possible time difference: ")
        int_max = input("Highest possible time difference: ")
    else:
        int_min = input("Lowest possible integer: ")
        int_max = input("Highest possible integer: ")

    check_for_quit([int_min.lower(), int_max.lower()])

    only_integers = False
    if selected_problem_type == "division":
        only_integers = input("Integer results only? [y/n]:\n")
        only_integers = True if "y" in only_integers.lower() else False
    significant_digits = 0
    if selected_problem_type in ["division", "square_root", "logarithm"] and not only_integers:
        significant_digits = int(
            input("Significant digits (0 for integer solutions):\n")
        )
    print("")

    # check that the provided limits are actually integers, else prompt for it again
    try:
        int_min, int_max = [int(limit) for limit in [int_min, int_max]]
    except ValueError:
        print("Bad input detected. The limits must be integer numbers")
        continue
    else:
        break

# initiate counts, lists and integer limits
problem_list = []

# run the problem generating loop
while True:
    if Problem.instance_count % 10 == 9 or Problem.instance_count == 0:
        print(f"--- Problem {Problem.instance_count + 1} -------------", end="")
    else:
        print("----------------------------", end="")

    # generate a problem with given parameters
    problem_generator = ProblemGenerator(
        problem_type=selected_problem_type,
        text_or_aloud=game_mode_as_text_or_aloud,
        int_min=int_min,
        int_max=int_max,
        significant_digits=significant_digits,
        only_integers=only_integers,
    )
    problem = problem_generator.generate_problem()

    # present the problem
    problem_interactor = ProblemIO(problem)
    problem_interactor.print_problem()

    # get answer as user input, determine if done playing and print feedback
    is_done_playing = problem_interactor.take_problem_answer_as_input()
    if is_done_playing:
        break
    problem_interactor.print_feedback_on_answer()
    problem_list.append(problem)

# compute and print mean response time
if len(problem_list) > 0:
    mean_time = np.mean([prob.time for prob in problem_list])
    performance_score = calculate_overall_performance_score(problem_list)
    correct_answers = sum([prob.answer_is_correct for prob in problem_list])
    print("\n-------------------------------------------", end="\n")
    print("----------------- RESULTS -----------------", end="\n")
    print("-------------------------------------------\n", end="\n")
    print(
        f"{100 * correct_answers / Problem.instance_count:.1f}% correct ({correct_answers} out of {Problem.instance_count})"
    )
    print(f"Average response time: {np.mean(mean_time):.2f} seconds")
    print(f"Overall performance score (0 - 100): {performance_score:.0f}")

    # turn into a dataset
    df = pd.DataFrame(
        {
            "time": [prob.time for prob in problem_list],
            "num1": [prob.num1 for prob in problem_list],
            "num2": [prob.num2 for prob in problem_list],
            "result": [prob.result for prob in problem_list],
            "answer": [prob.answer for prob in problem_list],
            "date": [prob.date for prob in problem_list],
            "correct": [prob.answer_is_correct for prob in problem_list],
            "score": [prob.score for prob in problem_list],
            "problem_type": [prob.problem_type for prob in problem_list],
            "text_or_aloud": [prob.text_or_aloud for prob in problem_list],
        }
    )
else:
    quit()

if quick_start_or_with_save_file == "quick" and len(problem_list) > 0:
    df_to_print = pd.DataFrame(
        {
            "mean": np.mean(df["time"]),
            "median": np.median(df["time"]),
            "std": np.std(df["time"]),
        },
        index=[0],
    )
    print("\nResponse time (seconds):\n", df_to_print.round(3))
    # ask if user wishes to save results to a file
    input_savefile = input("Save your results to a file? [y/n]: \n")
    check_for_quit(input_savefile.lower())

    # if yes, print list of already existing csv files in directory to save to
    if input_savefile.lower().startswith("y"):
        print("----------------------------------------")
        print("The following data files were found already:\n")
        while True:
            files = [f for f in os.listdir(TRAINING_FILES_PATH) if f.endswith(".csv")]
            [print(idx + 1, f) for idx, f in enumerate(files)]
            file = input("Write the name or number of the file you wish to use:\n")
            # check the given input and convert to integer if a number was given
            try:
                file = int(file)
            except ValueError:
                # if input is empty ask user to provide a better filename
                if all(i == " " for i in file):
                    print(
                        "\nEmpty input detected. Please provide a filename or number\n"
                    )
                    continue
                file = file if file.endswith(".csv") else file + ".csv"
                break
            # if integer input
            else:
                idx = file - 1
                file = files[idx]
                break

        write_mode = "a" if file in files else "w"  # append or write
        df.to_csv(
            TRAINING_FILES_PATH / file,
            index=False,
            mode=write_mode,
            header=write_mode == "w",
        )
    else:
        quit()

# else simply save to the file specified in the beginning
elif quick_start_or_with_save_file == "savefile" and len(problem_list) > 0:
    df.to_csv(TRAINING_FILES_PATH / file, index=False, mode="a", header=not file_exists)

df1 = pd.read_csv(TRAINING_FILES_PATH / file)

# mean and standard deviation analysis of response times
dates = df1.date.unique()
date_arrays = [df1[df1["date"] == date][["time", "score", "date"]] for date in dates]

# print mean and sd
df5 = pd.DataFrame(
    [
        (
            np.mean(dates.time),
            np.median(dates.time),
            np.std(dates.time),
            np.mean(dates.score),
            dates.date.unique(),
        )
        for dates in date_arrays
    ],
    columns=["mean", "median", "sd", "score", "date"],
)
print(df5)

# perform t-test with unequal variances
first = date_arrays[0].time
last = date_arrays[-1].time

t_test = stats.ttest_ind(first, last, equal_var=True)
significant_difference = t_test.pvalue <= 0.05
str_to_print = (
    f"Result: significant difference detected"
    if significant_difference
    else "Result: no significant difference detected"
)

print("\n\n-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("T-test for difference between first and last practice session timings")
print("-----------------------------------------------------------------------")
print(f"p-value: {t_test.pvalue:2f}")
print(str_to_print)
print("-----------------------------------------------------------------------")

# plot timing distributions
sns.set(color_codes=True)
sns.kdeplot(first, label="First")
sns.kdeplot(last, label="Latest")
plt.legend()
plt.title("Timing distributions")
plt.xlabel("Seconds")
plt.ylabel("Frequency")
plt.show()
