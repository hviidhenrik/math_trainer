# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 20:39:06 2020

@author: hviid
"""

'''
TO DO:
    - add timing of each problem
    - add unique ID of a problem (should be commutative) to be able to track
      improvements/difficulties on that particular question
    - add more math operations
    - make the while loop break if non-integer type is detected
    - implement different difficulty levels
'''


import numpy as np

class Problem:
    def __init__(self, num1, num2, operator):
        self.num1 = num1
        self.num2 = num2
        self.operator = operator
        self.answer = operator(num1, num2)
        self.id = "{}{}".format(num1,num2)
        
    def __str__(self):
        op = "+" if self.operator == np.add else "-" 
        return "{} {} {}".format(self.num1, op, self.num2)
    
    def __repr__(self):
        op = "+" if self.operator == np.add else "-" 
        return "{} {} {}".format(self.num1, op, self.num2)
    
#%% testing

count = 0
prob_array = []
while(count < 5):
    prob = Problem(np.random.randint(0,10), np.random.randint(0,10), np.add)
    prob_array.append(prob)
    input_answer = input("{} = ".format(prob))
    if input_answer.lower() == "stop":
        break
    elif prob.answer == int(input_answer):
        print("Correct")
    else:
        print("Incorrect")
    count += 1
