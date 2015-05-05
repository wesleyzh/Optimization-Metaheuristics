#particle swarm optimization


#need some python libraries
import copy
from random import Random
import math


#to setup a random number generator, we will specify a "seed" value
seed = 12345
myPRNG = Random(seed)


#best true solution is: f(x)=-n·418.9829; x(i)=420.9687, i=1:n.



#number of elements in a solution
n = 15

#population size
P=30

maxIteration = 1200

#min and max values for each element of the solution
xmin = -500
xmax = 500

wMax = 2
wMin = 0.25

c1 = 1.1
c2 = 0.5

vmax = 50

#function to evaluate a solution x
def evaluate(x):
    
    value = 0
    for i in xrange(0,n):
        value = value + (-x[i] * math.sin(math.sqrt(abs(x[i]))))
    
    return value
          
          
#start with a random solution
def random_particle():
    
    #initialize blank list
    x = []
    v = []
    
    #create solution (particle position)
    for i in xrange(0,n):
        x.append(myPRNG.uniform(xmin,xmax))
    
    #reserve the last two positions for value and best historical value
    for i in xrange(0,2):
        x.append(0)
        
    #create random direction (velocity)
    for i in xrange(0,n):
        v.append(myPRNG.random())
            
    return x[:], v[:]

#create an initial population of P particles
def initialize_population(P):

    population = []
    velocity = []
    individualBest = []

    for i in xrange(0,P):
        
        population.append(random_particle()[0])    #add particle to population      
        velocity.append(random_particle()[1])      #add particle to population      
        
    individualBest = population[:]
    
    return population, velocity, individualBest


def evaluate_population(population, individualBest):

    best = list(population[0])
    
    for i in xrange(0,len(population)):
                   
        val = evaluate(population[i])
        population[i][n] = val                   #evaluate particle        
        
        if val < population[i][n+1]:                 #if a pos better than particle's individual best
            individualBest[i] = list(population[i])
            population[i][n+1] = val
            individualBest[i][n+1] = val             #update individual best
            
        if val < best[n]:                        #find best in population
            best = list(population[i])
            
    return best
        

def update(population, velocity, individualBest, globalBest, iteration):
    
    w=wMax-((wMax-wMin)*iteration*1.0/maxIteration)  
    
    for i in xrange(0,P):
        for j in xrange(0,n):
            
            r1 = myPRNG.random()
            r2 = myPRNG.random()
            
            velocity[i][j] = w*velocity[i][j] + c1*r1*(indB[i][j]-population[i][j]) + c2*r2*(globalBest[j]-population[i][j])
            if velocity[i][j] > vmax:
                velocity[i][j] = vmax
             
            if velocity[i][j] < -vmax:
                velocity[i][j] = -vmax        
                
            population[i][j] = population[i][j] + velocity[i][j]
        
            if population[i][j] > 500:
                population[i][j] = 500 - 5*myPRNG.random()
            elif population[i][j] < -500:
                population[i][j] = -500 + 5*myPRNG.random()           

#create initial population of P random particles
pos, vel, indB = initialize_population(P)
popBest = evaluate_population(pos, indB)
x_best = popBest[:]                  #x_best will hold the best solution 

#begin local search overall logic

iteration = 0
for i in xrange(0,maxIteration):
    
    iteration = iteration + 1
    update(pos,vel,indB,x_best, iteration)
    
            
    popBest = evaluate_population(pos, indB)
    if popBest[n] < x_best[n]:
        x_best = popBest[:]
        
         
    print "Best value in population: ", popBest[n]        
    
print "Best value found: ", x_best[n]
print "Best solution: ", x_best[0:n]

print "Optimal value: ", -n*418.9829
#print "Best solution: ", x_best
