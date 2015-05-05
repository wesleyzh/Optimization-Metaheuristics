#Tabu Search

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


#function to evaluate a solution x
def evaluate(x):

    a=np.array(x)
    b=np.array(costs)
    c=np.array(weights)

    value = np.dot(a,b)          #compute the cost value of the knapsack selection
    totalWeight = np.dot(a,c)    #compute the weight value of the knapsack selection

    if totalWeight > maxWeight:
        value = -1

    return value, totalWeight


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



x_best = x_curr[:]   
f_curr = evaluate(x_curr)[0]
f_best = f_curr

#Tabu Search Variables
max_iter = 1000  #maximum iterations
tabu_tenure = 5  #tabu active for 3 iterations

tabu_list = {}  #initialize tabu memory
candidate = 70  #number of candidates chosen from neighoborhodd

for k in range(max_iter):
    
    Neighborhood = neighborhood(x_curr)   #create a list of all neighbors in the neighborhood of x_curr        

    candidate_dic= {}
    for i in range (candidate):
        temp =  myPRNG.choice(Neighborhood)
        candidate_dic[evaluate(temp)[0]] = temp
    
    Tabu = 0
    while Tabu == 0:
        
        best_candidate = max(candidate_dic.keys())
        s = candidate_dic[best_candidate]
        
        index = Neighborhood.index(s)        
        
        if index in tabu_list.keys():
            if best_candidate > f_best:    #aspiration criteria
                x_best = s[:]              #find the best member and keep track of that solution
                f_best = evaluate(s)[0]       #and evaluation value
                x_curr = s[:]              #make a move
                f_curr = evaluate(s)[0]
                del tabu_list[index]
                Tabu = 1
            else:
                del candidate_dic[best_candidate]
        else:
            if best_candidate > f_best:    #aspiration criteria
                x_best = s[:]              #find the best member and keep track of that solution
                f_best = evaluate(s)[0]       #and evaluation value
            x_curr = s[:]              #make a move
            f_curr = evaluate(s)[0]
            tabu_list[index] = tabu_tenure
            Tabu = 1
    
    #update tabu list
    for key, value in tabu_list.items():
        if value == 1:
            del tabu_list[key]
        else:
            tabu_list[key] = value - 1
    
            

print "Best value found: ", f_best
print "Total weight:", evaluate(x_best)[1]
print "Best solution: ", x_best
    
    



