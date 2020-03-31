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
        self.time = np.nan
        # self.id = "{}{}".format(num1, num2) # not implemented yet
        
    def __str__(self):
        op = "+" if self.operator == np.add else "-" 
        return "{} {} {}".format(self.num1, op, self.num2)
    
    def __repr__(self):
        op = "+" if self.operator == np.add else "-" 
        return "{} {} {}".format(self.num1, op, self.num2)
    
#%% testing
from timeit import default_timer as timer

# print an overview of alread existing csv files in directory

# ask which one to save to, or make a new one
    # if existing one chosen, append results
    # else make new file

count = 0
corrects = 0
prob_array = []
time_array = []
answer_array = []
int_min = input("Lowest possible integer: ")
int_max = input("Highest possible integer: ")
while(1):
    prob = Problem(np.random.randint(int_min,int_max), 
                   np.random.randint(int_min,int_max), 
                   np.add)
    start = timer()
    input_answer = input("{} = ".format(prob))
    if input_answer.lower() == "stop":
        end = timer()
        break
    elif prob.result == int(input_answer):
        print("Correct")
        corrects += 1
    else:
        print("Incorrect")
    end = timer()
    prob.time = end - start
    time_array.append(end-start)
    count += 1
    prob_array.append(prob)
    answer_array.append(int(input_answer))


print("{}% correct ({} out of {})".format(np.round(100*corrects/count,2), corrects, count))
print("Average repsonse time: ", np.round(np.mean(time_array),2), "seconds")

#%% turn into a dataset
import pandas as pd

df = pd.DataFrame({"time": time_array,
                   "num1":   [prob.num1 for prob in prob_array],
                   "num2":   [prob.num2 for prob in prob_array],
                   "result": [prob.result for prob in prob_array],
                   "answer": answer_array})
df["correct"] = [1 if diff == 0 else 0 for diff in df.answer - df.result] # codes it as binary integers

df.to_csv("math_practice.csv", sep="\t",)

#%% analysis
from sklearn import linear_model

df.columns
X = df[["num1","num2","result","answer","correct"]]
X = df[["correct"]]
y = df["time"]

regr = linear_model.LinearRegression()
regr.fit(X,y)
regr.coef_


#%% own model analysis
from scipy import stats
lm = LinearRegression()
lm.fit(X,y)
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
