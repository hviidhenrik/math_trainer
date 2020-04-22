# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 20:39:06 2020

@author: hviid

TO DO:
    - add option to cancel choice in input, e.g. if saving to a file, cancel it
        if "cancel" or "stop" is detected as file name
    - improve integer division mode to give actually non-trivial problems that arent 
        a/1 or a/a - prevent prime numbers
    - implement a true division mode where results can be rounded fractions, e.g. 0.33
    - make graphical interface
    - catch empty input when selecting file to save
    - ensure that results can only be saved to files with the same game mode,
       e.g. addition, multiplication etc) to avoid data getting mixed up -
       alternatively, add a column in the data that shows the operation for
       each problem/row
    - add option to "go back" when selecting game mode, whether to save and such
    - add hidden "quit option" to all input prompts
"""

import numpy as np
from datetime import date

# define a problem class
class Problem:
    instance_count = 0
    def __init__(self, num1, num2, operator):
        Problem.instance_count += 1
        self.num1 = num1
        self.num2 = num2
        self.operator = operator # should be a function such as np.add
        
        # prevent division by zero
        if self.operator == np.divide and self.num2 == 0:
            self.num2 += 1
        
        self.result = np.round(operator(self.num1, self.num2),2) # the correct result
        self.answer = np.nan  # the user provided answer
        self.error = np.nan   # how far off the provided answer is
        self.time = np.nan    # how long it took to answer
        self.date = date.today().strftime("%b-%d-%Y")
        
    def __str__(self):
        if self.operator == np.add:
            op = "+"
        elif self.operator == np.multiply:
            op = "x"
        elif self.operator == np.divide:
            op = "/"
            
        return "{} {} {}".format(self.num1, op, self.num2)
    
    def __repr__(self):
        # op = "+" if self.operator == np.add else "-" 
        if self.operator == np.add:
            op = "+"
        elif self.operator == np.multiply:
            op = "x"
        elif self.operator == np.divide:
            op = "/"
        return "{} {} {}".format(self.num1, op, self.num2)
    
    def __del__(self):
        Problem.instance_count -= 1
        
# helper function to take validate and take integer input from the user   
def input_number(message,exception_message = None):
    # if no exception message is provided, use a standard one
    if exception_message is None:
            exception_message = "Bad input detected. Please provide an integer"
    # loop to check for and obtain proper integer input
    while True:
        user_input = input(message)
        try:
            user_input = int(user_input)
        except ValueError:
            print(exception_message)
            continue
        else:
            break
    return user_input
    
#%% setup for saving to a file or not
        
import os

# prompt the user whether to quick start or use existing/new file and check input

    
print("WELCOME TO MATH TRAINER v1.0")
print("----------------------------")
print("How would you like to play?\n")
    
    
    # print("Quick start (q) or save results to existing/new file (e)?\n")
    
    # start = input("Quick start (q) or save results to existing/new file (e)?\n")
while True:
    print("[1] Quick start")
    print("[2] Create/select a file to save to")
    start = input("Your choice: ")
    print("----------------------------\n")
    
    # check the input for validity
    
    ##
    modes = {"1":"quick", "2":"savefile","q":"quit"}
    print()
    # validate input and prompt user again if erroneous input was detected
    try:
        start = modes[start]
    except KeyError:
        print("Bad input detected. Must be either 1 or 2\n")
    # hidden quit option (mostly for my own testing purposes)
    else:
        if start == "quit":
            raise SystemExit
        else:
            break
            
# if existing/new file was chosen, let user decide the file to save to
if start == "savefile":
        # print an overview of already existing csv files in directory
    print("\nThe following data files were found already:\n")
    while True:
        files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(".csv")]
        [print("[", idx+1,"] ",f,sep="") for idx, f in enumerate(files)]
    
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

#%% main section that runs the practice loop
from timeit import default_timer as timer


# initiate counts, lists and integer limits
count = 0
corrects = 0
prob_array = []

# get desired math operation using input and a predefined dictionary of operations
while True:
    print("[1] Addition/subtraction")
    print("[2] Multiplication")
    print("[3] Division")
          
    operator = input("Your choice: ")
    print("----------------------------\n")
    
    # operator = input("Addition/subtraction, multiplication or division? [a/m/d]\n")
    # ops = {"a":np.add, "m":np.multiply, "d":np.divide}
    ops = {"1":np.add, "2":np.multiply, "3":np.divide}
    
    # validate input and prompt user again if erroneous input was detected
    try:
        operator = ops[operator]
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
        int_min, int_max = [int(limit) for limit in [int_min,int_max]]
    except ValueError:
        print("Bad input detected. The limits must be integer numbers")
        continue
    else:
        break


# run the problem generating loop
while True:
    if count % 10 == 9 or count == 0:
        print("--- Problem {} -------------".format(count+1),end="")
    else:
        print("----------------------------",end="")
    # initiate a problem instance
    if operator == np.divide:
        num1 = np.random.randint(int_min,int_max)
        
        # guard against fractional numbers and division by zero
        while True:
            num2 = np.random.randint(int_min,int_max)
            if num2 != 0 and np.divide(num1,num2) % 1 == 0:
                break
            
        prob = Problem(num1, num2, operator) # np.add originally
    else:
        prob = Problem(np.random.randint(int_min,int_max), 
                   np.random.randint(int_min,int_max), 
                   operator) # np.add originally
    
    # start timer
    timer_start = timer()
    
    # the answer from the user
    
    input_answer = input("{} = ".format(prob))
        
    # check the input - if 's' is detected, stop the loop
    if input_answer.lower().startswith("s"):
        timer_end = timer()
        del(prob)
        break
    # else try to convert the input to integer
    else:
        # try to convert given answer to integer else print message and pose new problem
        try:
            input_answer = int(input_answer)
        except ValueError:
            print("Bad input detected - please provide integer numbers or \"stop\" (s)")
            print("")
            del(prob)
            continue       
        
        # if provided answer is correct
        if prob.result == input_answer:
            print("Correct\n",end="\n")
            corrects += 1
        # if it's not correct
        else:
            print("Incorrect\n",end="\n")
        
    # store timing, problem and answer and increment problem count
    timer_end = timer()
    prob.time = timer_end-timer_start
    count += 1
    prob_array.append(prob)
    prob.answer = input_answer

# compute and print mean response time
if len(prob_array) > 0:
    mean_time = np.mean([prob.time for prob in prob_array])
    print("\n-------------------------------------------",end="\n")
    print("----------------- RESULTS -----------------",end="\n")
    print("-------------------------------------------\n",end="\n")
    print("{}% correct ({} out of {})".format(np.round(100*corrects/count,2), corrects, count))
    print("Average response time: ", np.round(np.mean(mean_time),2), "seconds")

#%% turn into a dataset
import pandas as pd

df = pd.DataFrame({"time":   [prob.time for prob in prob_array],
                   "num1":   [prob.num1 for prob in prob_array],
                   "num2":   [prob.num2 for prob in prob_array],
                   "result": [prob.result for prob in prob_array],
                   "answer": [prob.answer for prob in prob_array],
                   "date":   [prob.date for prob in prob_array]})
df["correct"] = [1 if diff == 0 else 0 for diff in df.answer - df.result] # codes it as binary integers
df["operation"] = operator

#%% for adding new columns to existing data - NOT RUN! 
# filename88 = "filename-goes-here.csv"
# df88 = pd.read_csv(filename88)
# df88["operation"] = np.multiply
# df88.to_csv(filename88,index=False)
# df99 = pd.read_csv(filename88)
# df99
#%% writing or appending to a file

# if quick start was chosen in the beginning prompt for saving
if start == "quick" and len(prob_array) > 0:
    # ask if user wishes to save results to a file
    input_savefile = input("Save your results to a file? [y/n]\n")
    
    # if yes, print list of already existing csv files in directory to save to
    if input_savefile.lower().startswith("y"):
        # print an overview of already existing csv files in directory
        print("----------------------------------------")
        print("The following data files were found already:\n")
        while True:
            files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(".csv")]
            [print(idx+1,f) for idx, f in enumerate(files)]
        
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
            
        mode = "a" if file in files else "w" # append or write
        df.to_csv(file, index = False, mode = mode, header = mode == "w")

# else simply save to the file specified in the beginning
elif start == "savefile" and len(prob_array) > 0:
    df.to_csv(file, index = False, mode = "a", header = not file_exists)

df1 = pd.read_csv(file)
# # df1
# # df.to_csv("math_practice.csv",index=False)
print("")
print(df1)


#%% quick analysis
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

dates = df1.date.unique()
date_arrays = [df1[df1["date"] == date][["time","date"]] for date in dates]

# print mean and sd
df5 = pd.DataFrame([(np.mean(dates.time),
                      np.std(dates.time),
                      dates.date.unique()) for dates in date_arrays],
                    columns=["mean","sd","date"])
print(df5)

# perform t-test with unequal variances
first = date_arrays[0].time
last = date_arrays[-1].time

stats.ttest_ind(first,last,equal_var=False)


# plot timing distributions
sns.set(color_codes=True)
sns.kdeplot(first,label="First")
sns.kdeplot(last,label = "Latest")
plt.legend()
plt.title("Timing distributions")
plt.xlabel("Seconds")
plt.ylabel("Frequency")



