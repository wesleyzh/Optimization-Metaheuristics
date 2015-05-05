#hill climbing search


#need some python libraries
import copy
from random import Random
import numpy as np


#to setup a random number generator, we will specify a "seed" value
seed = 12345
myPRNG = Random(seed)

#to get a random number between 0 and 1, write call this:             myPRNG.random()
#to get a random number between lwrBnd and upprBnd, write call this:  myPRNG.uniform(lwrBnd,upprBnd)
#to get a random integer between lwrBnd and upprBnd, write call this: myPRNG.randint(lwrBnd,upprBnd)


#number of elements in a solution
n = 100



#let's create an instance for the knapsack problem
costs = []
for i in xrange(0,n):
    costs.append(myPRNG.randint(10,100))
    
weights = []
for i in xrange(0,n):
    weights.append(myPRNG.randint(5,15))
    
#define max weight for the knapsack
maxWeight = 5*n


#monitor the number of solutions evaluated
solutionsChecked = 0


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
          


#define the solution variables
x_curr = [] #x_curr will hold the current solution 

#f_curr will hold the "fitness" of the current soluton 
#x_best will hold the best solution 


#start with a random solution
for i in xrange(0,n):
    #x_curr.append(myPRNG.randint(0,1))
    
    if myPRNG.random() < 0.7:
        x_curr.append(0)
    else:
        x_curr.append(1)
        
    

#begin local search overall logic

done = 0

x_best = x_curr[:]   
f_curr = evaluate(x_curr)
f_best = f_curr
    
while done == 0:
        
    
    #print len(neighborhood(x_curr))    
    
    Neighborhood = neighborhood(x_curr)   #create a list of all neighbors in the neighborhood of x_curr
    
    for s in Neighborhood:             #evaluate every member in the neighborhood of x_curr
        solutionsChecked = solutionsChecked + 1
        if evaluate(s) > f_best:   
            x_best = s[:]              #find the best member and keep track of that solution
            f_best = evaluate(s)       #and evaluation value
            break                      #stop the loop with the first improvement solution
    
    if f_best == f_curr:               #if there were no improving solutions in the neighborhood
        done = 1
    else:
        print "\nTotal number of solutions checked: ", solutionsChecked
        print "Best value found: ", f_best
        print "Best solution: ", x_best        
        x_curr = x_best[:]         #else: move to the neighbor solution and continue
        f_curr = f_best            #evalute the current solution
    
print "\nTotal number of solutions checked: ", solutionsChecked
print "Best value found: ", f_best
print "Best solution: ", x_best
