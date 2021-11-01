# Math Trainer

## Purpose and idea

Welcome to Math Trainer. When this project started in early 2020, 
the purpose of this Python program was twofold:
 1) To train my python skills
 2) To train my mental math skills

However, nowadays I've learned Python much more through my 
work, so the purpose is now just to train my mental math 
abilities. 

The program is easy to use. Simply run main.py and the 
prompt will guide you through the rest of the process 
from choosing a type of math problem to which file to save 
your results to. 

## To be added

New types of problems are added every now and then, when 
I feel like it. The current back log of things to do is 
as listed below:

- implement time difference mode, e.g. hours between 22 and 8
- implement log approximation mode
- implement "mixed mode" which poses a random mix of selected problem types
- implement percentage approximation mode. The approximation error could 
  then be used instead of binary correct/incorrect as measure of performance
- make a unified performance score. Could just be the average of the response times t_i weighted by 
  1 if incorrect and -1 if correct, call this s_i. Invert this by subtracting each of these products
  from the max: max_i(s_i * t_i) - s_i * t_i. To aggregate into a single number, simply average it.
- make response time appear below the "correct/incorrect" feedback of each problem.  
- make graphical interface (probably never gonna happen)
- make text-to-speech so problems are read aloud better simulating a 
  day to day example situation of mental math 