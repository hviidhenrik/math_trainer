# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 20:39:06 2020

@author: hviid

TO DO:
    - add unique ID of a problem (should be commutative?) to be able to track
      improvements/difficulties on that particular question nad how many times
      it has been answered
    - add more math operations
    - implement different difficulty levels
"""


import numpy as np

class Problem:
    instance_count = 0
    def __init__(self, num1, num2, operator):
        Problem.instance_count += 1
        self.num1 = num1
        self.num2 = num2
        self.operator = operator
        self.answer = operator(num1, num2)
        self.time = np.nan
        self.id = "{}{}".format(num1, num2)
        
    def __str__(self):
        op = "+" if self.operator == np.add else "-" 
        return "{} {} {}".format(self.num1, op, self.num2)
    
    def __repr__(self):
        op = "+" if self.operator == np.add else "-" 
        return "{} {} {}".format(self.num1, op, self.num2)
    
#%% testing
from timeit import default_timer as timer

count = 0
corrects = 0
prob_array = []
time_array = []
int_min = input("Lowest possible integer: ")
int_max = input("Highest possible integer: ")
while(1):
    prob = Problem(np.random.randint(int_min,int_max), 
                   np.random.randint(int_min,int_max), 
                   np.add)
    prob_array.append(prob)
    start = timer()
    input_answer = input("{} = ".format(prob))
    if input_answer.lower() == "stop":
        end = timer()
        break
    elif prob.answer == int(input_answer):
        print("Correct")
        corrects += 1
    else:
        print("Incorrect")
    end = timer()
    prob.time = end - start
    time_array.append(end-start)
    count += 1


print("{}% correct ({} out of {})".format(np.round(100*corrects/count,2), corrects, count))
print("Average repsonse time: ", np.round(np.mean(time_array),2), "seconds")


