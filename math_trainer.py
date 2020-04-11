# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 20:39:06 2020

@author: hviid

TO DO:
    - add more math operations
    - implement different difficulty levels
    - make graphical interface
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
        self.result = operator(num1, num2)
        self.answer = np.nan
        self.time = np.nan
        self.date = date.today().strftime("%b-%d-%Y")
        
    def __str__(self):
        op = "+" if self.operator == np.add else "-" 
        return "{} {} {}".format(self.num1, op, self.num2)
    
    def __repr__(self):
        op = "+" if self.operator == np.add else "-" 
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
while True:
    start = input("Quick start (q) or save results to existing/new file (e)?\n")
    # check the input for validity
    try:
        start = start[0].lower()
    except IndexError:    
        print("Bad input, please provide wether to use quick start or new/existing file [q/e]\n")
        continue
    else:
        if start in ["q","e"]:
            break

# if existing/new file was chosen, let user decide the file to save to
if start == "e":
    # print an overview of already existing csv files in directory
    print("The following data files were found already:\n")
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(".csv")]
    [print(idx+1,f) for idx, f in enumerate(files)]

    # prompt the user for a desired file
    file = input("Write the name or number of the file you wish to use:\n")
    
    # check the given input and convert to integer if a number was given
    try:
        file = int(file)
    # exception raised if it is a string input
    except ValueError:
        file = file if file.endswith(".csv") else file + ".csv"
        # check if the file exists to determine the inclusion of a header in csv
        file_exists = file in files 
    # if integer input
    else:
        idx = file - 1
        file = files[idx]
        file_exists = True

#%% main section that runs the practice loop
from timeit import default_timer as timer


# initiate counts, lists and integer limits
count = 0
corrects = 0
prob_array = []

# get upper and lower limits of the math problems to be posed
while True:
    int_min = input("Lowest possible integer: ")
    int_max = input("Highest possible integer: ")
    
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
    # if count % 9 == 0:
    #     print("--- Problem {} ---".format(count+1),end="")
    # initiate a problem instance
    prob = Problem(np.random.randint(int_min,int_max), 
                   np.random.randint(int_min,int_max), 
                   np.add)
    
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
            del(prob)
            continue       
        
        # if provided answer is correct
        if prob.result == input_answer:
            print("Correct")
            corrects += 1
        # if it's not correct
        else:
            print("Incorrect")
        
    # store timing, problem and answer and increment problem count
    timer_end = timer()
    prob.time = timer_end-timer_start
    count += 1
    prob_array.append(prob)
    prob.answer = input_answer

# compute and print mean response time
if len(prob_array) > 0:
    mean_time = np.mean([prob.time for prob in prob_array])
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

#%% writing or appending to a file

# if quick start was chosen in the beginning prompt for saving
if start == "q" and len(prob_array) > 0:
    # ask if user wishes to save results to a file
    input_savefile = input("Save your results to a file? [y/n]\n")
    
    # if yes, print list of already existing csv files in directory to save to
    if input_savefile.lower().startswith("y"):
        # print an overview of already existing csv files in directory
        print("----------------------------------------")
        print("The following data files were found already:\n")
        files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(".csv")]
        [print(idx+1,f) for idx, f in enumerate(files)]
    
        # prompt the user for a desired file
        file = input("Write the name or number of the file you wish to use:\n")
        
        # check the given input and convert to integer if a number was given
        try:
            file = int(file)
        # exception raised if it is a string input
        except ValueError:
            file = file if file.endswith(".csv") else file + ".csv"
        # if integer input
        else:
            idx = file - 1
            file = files[idx]
        
        mode = "a" if file in files else "w" # append or write
        df.to_csv(file, index = False, mode = mode, header = mode == "w")

# else simply save to the file specified in the beginning
elif start == "e" and len(prob_array) > 0:
    df.to_csv(file, index = False, mode = "a", header = not file_exists)

df1 = pd.read_csv(file)
# # df1
# # df.to_csv("math_practice.csv",index=False)

print(df1)

#%% 

from tkinter import *
root = Tk() 
root.geometry('300x600') 
root.title("First Tkinter Window") 
root.mainloop() 
