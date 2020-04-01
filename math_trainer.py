# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 20:39:06 2020

@author: hviid

TO DO:
    - add unique ID of a problem (should be commutative?) to be able to track
       improvements/difficulties on that particular question and how many times
       it has been answered
    - add more math operations
    - implement different difficulty levels
    - add exception to handle empty input as in if user just pushes enter 
       and nothing else 
    - make quick start mandatory if directory is empty
"""


import numpy as np

class Problem:
    instance_count = 0
    def __init__(self, num1, num2, operator):
        Problem.instance_count += 1
        self.num1 = num1
        self.num2 = num2
        self.operator = operator
        self.result = operator(num1, num2)
        self.answer = np.nan
        self.time = np.nan
        
    def __str__(self):
        op = "+" if self.operator == np.add else "-" 
        return "{} {} {}".format(self.num1, op, self.num2)
    
    def __repr__(self):
        op = "+" if self.operator == np.add else "-" 
        return "{} {} {}".format(self.num1, op, self.num2)
    
    def __del__(self):
        Problem.instance_count -= 1
    
#%% 
import os
quick_start = input("Quick start or use existing file? [quick/existing]\n")
quick_start = quick_start.lower().startswith("q")


if not quick_start:
    # print an overview of already existing csv files in directory
    print("The following data files were found already:")
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(".csv")]
    print(files)
    file = input("Write the name of the file you wish to use:\n")
    file = file if file.endswith(".csv") else file + ".csv"


#%% testing
from timeit import default_timer as timer


# init counts and lists
count = 0
corrects = 0
prob_array = []
int_min = input("Lowest possible integer: ")
int_max = input("Highest possible integer: ")

# run the main game/practice loop
while(1):
    prob = Problem(np.random.randint(int_min,int_max), 
                   np.random.randint(int_min,int_max), 
                   np.add)
    start = timer()
    input_answer = input("{} = ".format(prob))
    
    # if the user wishes to stop the game
    if input_answer.lower() == "stop":
        end = timer()
        del(prob)
        break
    
    # if provided answer is correct
    elif prob.result == int(input_answer):
        print("Correct")
        corrects += 1
    # if it's not correct
    else:
        print("Incorrect")
        
    # store timing, problem and answer and increment problem count
    end = timer()
    prob.time = end-start
    count += 1
    prob_array.append(prob)
    prob.answer = int(input_answer)

# compute mean response time
mean_time = np.mean([prob.time for prob in prob_array])

# print some stats
print("{}% correct ({} out of {})".format(np.round(100*corrects/count,2), corrects, count))
print("Average response time: ", np.round(np.mean(mean_time),2), "seconds")

#%% turn into a dataset
import pandas as pd

df = pd.DataFrame({"time":   [prob.time for prob in prob_array],
                   "num1":   [prob.num1 for prob in prob_array],
                   "num2":   [prob.num2 for prob in prob_array],
                   "result": [prob.result for prob in prob_array],
                   "answer": [prob.answer for prob in prob_array]})
df["correct"] = [1 if diff == 0 else 0 for diff in df.answer - df.result] # codes it as binary integers

#%% writing or appending to a file

if quick_start:
    print("----------------------------------------")
    print("The following files were already found in the directory:")
    print(files)
    save_file = input("If you wish to save to an existing file seen above, simply type its name - otherwise, a new file will be created: \n")
    save_file = save_file if save_file.endswith(".csv") else save_file + ".csv"
    mode = "a" if save_file in files else "w" # append or write
    df.to_csv(save_file, index = False, mode = mode, header = mode == "w")
else:
    df.to_csv(file, index = False, mode = "a", header = False)

df1 = pd.read_csv("math_practice.csv")
# df1
# df.to_csv("math_practice.csv",index=False)

print(df1)

#%% statistical analysis
from sklearn import linear_model

df.columns
df.iloc[[1],5] = 0

X = df[["num1","num2","result","correct"]]
# X = df[["correct"]]
y = df["time"]

lm = linear_model.LinearRegression()
lm.fit(X,y)
lm.coef_




#%% own model analysis
from scipy import stats
params = np.append(lm.intercept_,lm.coef_)
predictions = lm.predict(X)

newX = pd.DataFrame({"Constant":np.ones(len(X))}).join(pd.DataFrame(X))
MSE = (sum((y-predictions)**2))/(len(newX)-len(newX.columns))

# Note if you don't want to use a DataFrame replace the two lines above with
# newX = np.append(np.ones((len(X),1)), X, axis=1)
# MSE = (sum((y-predictions)**2))/(len(newX)-len(newX[0]))

var_b = MSE*(np.linalg.inv(np.dot(newX.T,newX)).diagonal())
sd_b = np.sqrt(var_b)
ts_b = params/ sd_b
p_values =[2*(1-stats.t.cdf(np.abs(i),(len(newX)-1))) for i in ts_b]

sd_b = np.round(sd_b,3)
ts_b = np.round(ts_b,3)
p_values = np.round(p_values,3)
params = np.round(params,4)

myDF3 = pd.DataFrame()
myDF3["Coefficients"],myDF3["Standard Errors"],myDF3["t values"],myDF3["Probabilites"] = [params,sd_b,ts_b,p_values]
print(myDF3)
