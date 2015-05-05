#Simulated Annealing Search with Cauchy Schedule

#need some python libraries
import copy
from random import Random
import numpy as np
import math
import time

def Update_Tem(T0, itval):
    
    T = T0 / (1 + itval)
    
    return T

#function to evaluate a solution x
def evaluate(x):
    
    
    a=np.array(x)
    b=np.array(costs)
    c=np.array(weights)

    value = np.dot(a,b)          #compute the cost value of the knapsack selection
    totalWeight = np.dot(a,c)    #compute the weight value of the knapsack selection

    if totalWeight > maxWeight:
        value = -1

    return value

#function to create a 1-flip neighborhood of solution x         
def neighborhood(x):

    nbrhood = []     

    for i in xrange(0,n):
        nbrhood.append(x[:])
        if nbrhood[i][i] == 1:
            nbrhood[i][i] = 0
        else:
            nbrhood[i][i] = 1

    return nbrhood


    
#to setup a random number generator, we will specify a "seed" value
seed = 12345
myPRNG = Random(seed)

#number of elements in a solution
n = 100


#SA parameters
T0 = 100000      #initial temperature
M = 20           #the number of iterations for each temperature
max_Iter = 1000  #maximum number of iterations

#let's create an instance for the knapsack problem
costs = []
for i in xrange(0,n):
    costs.append(myPRNG.randint(10,100))
    
weights = []
for i in xrange(0,n):
    weights.append(myPRNG.randint(5,15))
    
#define max weight for the knapsack
maxWeight = 5*n

#define the solution variables
x_curr = [] #x_curr will hold the current solution     


#start with a random solution
for i in xrange(0,n):
    #x_curr.append(myPRNG.randint(0,1))
    
    if myPRNG.random() < 0.7:
        x_curr.append(0)
    else:
        x_curr.append(1)    

        
        

        
x_best = x_curr[:]   
f_curr = evaluate(x_curr)
f_best = f_curr

for k in range(1, max_Iter+1):
    
    T = Update_Tem(T0, k)
    
    Neighborhood = neighborhood(x_curr)   #create a list of all neighbors in the neighborhood of x_curr        
    
    m = 0
    while m < M:
        s = myPRNG.choice(Neighborhood)
        
        if evaluate(s) > f_best:   
            x_best = s[:]              #find the best member and keep track of that solution
            f_best = evaluate(s)       #and evaluation value
            x_curr = s[:]              #make a move
            f_curr = evaluate(s)
        else:
            delta =  evaluate(x_curr) - evaluate(s)       #difference between the objective values
            
            if myPRNG.random() < math.exp(-1*delta/T):   
                x_curr = s[:]          #make a move
                f_curr = evaluate(s)
                
        m += 1
    
print "Final Temperature", T
print "Best value found: ", f_best
print "Best solution: ", x_best
