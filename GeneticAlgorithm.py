'''
Modified Genetic Algorithm for Network Resilience Problem
Impleted by weili zhang, 2014-09-16
references: Lee, W., & Kim, H. Y. (2005). Genetic algorithm implementation in Python. 

Input:
nodes_list = list of nodes
edge_list = list of existed edges
u = population of each node
q = reliability of each link
BinVar = binary variables list, in this case, it is the list of given by the paper
num_population = number of chromos per population
max_iteration = maximum iterations
max_time = maximum time
crossover_rate = probility of crossover
mutation_rate = probility of mutation

Output:
Best solution found
Best fitness value found

'''

import random, copy, time, operator
import RE
import friability_evaluation as FE
import passagewaysearch as PS

'''
#create an initial population
sample_chrm = range(1,10)  #a feasible solution
init_population = []       #an empty list
random.seed(0)
population_size = 5

for i in xrange(population_size):
    new_chrm = copy.copy(sample_chrm)
    random.shuffle(new_chrm)
    init_population.append(new_chrm)
    
#evaluate fitness values
cost_matrix = []     # an empty list
cost_matrix.append([0,0,0,0,0,0,0,0,0,0])
cost_matrix.append([0,0,1,5,6,9,2,3,7,8])
cost_matrix.append([0,1,0,8,6,2,4,7,9,5])
cost_matrix.append([0,5,8,0,3,2,7,6,8,9])
cost_matrix.append([0,6,6,3,0,9,7,4,1,5])
cost_matrix.append([0,9,2,2,9,0,1,4,7,3])
cost_matrix.append([0,2,4,7,7,1,0,7,4,1])
cost_matrix.append([0,3,7,6,4,4,7,0,8,3])
cost_matrix.append([0,7,9,8,1,7,4,8,0,1])
cost_matrix.append([0,8,5,9,5,3,1,3,1,0])

chrm = [4, 1, 5, 6, 9, 2, 3, 7, 8]
cost = 0
last_city = chrm[0]
for current_city in chrm:
    cost += cost_matrix[last_city][current_city]
    last_city = current_city


#selection
import operator
fitness_list = [6.0, 9.0, 4.0, 3.0, 5.0, 8.0, 3.0, 6.0, 3.0, 3.0]
fitness_sum = reduce( operator.add, fitness_list)
print sum(fitness_list)
print fitness_sum

prob_list = map( (lambda x: x/fitness_sum), fitness_list) 
print prob_list

cum_value = 0
cum_prob_list = []
for prob in prob_list:
    cum_prob_list.append( cum_value + prob )
    cum_value += prob
    
print cum_prob_list    
cum_prob_list[-1] = 1.0

selected = []
size = 100
for i in xrange(size):
    rn = random.random()
    for j, cum_prob in enumerate(cum_prob_list):
        if rn<= cum_prob:
            selected.append( j)
            break
    
print selected

#double point crossover
parent1 = [ 1, 0, 1, 1, 0, 1, 1, 1 ]
parent2 = [ 0, 1, 0, 0, 1, 0, 1, 1 ]

pt1 = 2 # crossover point 1
pt2 = 5 # crossover point 2

offspring1 = parent1[:pt1] + parent2[pt1:pt2] + parent1[pt2:]
print parent1[:pt1], parent2[pt1:pt2], parent1[pt2:]
offspring2 = parent2[:pt1] + parent1[pt1:pt2] + parent2[pt2:]

#mutation
#insert mutation
chrm = [4, 1, 5, 6, 9, 2, 3, 7, 8]
element_position = random.randint(0, len(chrm)-1 )
insert_position = random.randint(0, len(chrm)-2 )
element_value = chrm[element_position]
del chrm[element_position]
chrm.insert( insert_position, element_value )

#exchange mutation
chrm = [4, 1, 5, 6, 9, 2, 3, 7, 8]
position1 = random.randint(0, len(chrm)-1 )
position2 = random.randint(0, len(chrm)-1 )
chrm[position1], chrm[position2] = chrm[position2], chrm[position1]
'''

def generate_population(BinVar, num_population, investment):
    
    '''generate the first random population'''
    
    #remove the duplicated link index from BinVar, split binary variables to BinVar1 and BinVar2
    BinVar1,BinVar2 = [], []
    for (i,j) in BinVar:
        if (j,i) not in BinVar1:
            BinVar1.append((i,j))
        else:
            BinVar2.append((i,j))    
            
    
    chromos = {}    
    for eachChromo in range(num_population):
        chromo1, chromo2 = {}, {}    #chromo1 is the main chromo and chromo2 is the corresponding reverse index variable
        for (i,j) in BinVar1:
	    if random.random() < float(investment/170.00):
		chromo1[i,j] = 1 #random.randint(0,1)
		chromo2[j,i] = chromo1[i,j]          #chromo2 is the revers index but same link
	    else:
		chromo1[i,j] = 0 #random.randint(0,1)
		chromo2[j,i] = chromo1[i,j]          #chromo2 is the revers index but same link		
        chromos[eachChromo] = dict(chromo1.items() + chromo2.items())
  
    return chromos


def fitness_evaluate(population, V_l, E_l, investment, GA_Reinfoce_open, GA_Construct_open, G):
    '''caculate the fitness value beased on equationn (22), constrain(20) is handled as a negetive penalty function'''
    chromos_fitness = {}
    
    if GA_Reinfoce_open == 1:   #reinforce current network
        for eachChromo in population.keys():
	    bridge_reliability = copy.deepcopy(G.resilience)
            for (i,j) in population[eachChromo].keys():
            #update resilience for corresponding bridge
                if population[eachChromo][i,j] == 1:
                    bridge_reliability[i,j] = 0.99
        
            #update the Fresilience_Path
            GAL, GALength_Path, GAFresilience_Path, GAPath_ADTT = PS.main(G.nodes,G.arcs, G.emergnode, G.length, bridge_reliability,G.ADTT)#normmalize the path length 	
	    GANormal_Path_Length = {}	
	    for headnode, tailnode in GALength_Path.keys():
		GANormal_Path_Length[headnode, tailnode] = {}
		if len(GALength_Path[headnode, tailnode].keys()) == 1:
		    GANormal_Path_Length[headnode, tailnode][1] = 1
		elif len(GALength_Path[headnode, tailnode].keys()) > 1:
		    Temp_Sum = 0
		    for k,value in GALength_Path[headnode, tailnode].items():
			Temp_Sum += value
		    Normal_sum = 0
		    for k,value in GALength_Path[headnode, tailnode].items():
			Normal_sum += Temp_Sum - value
		    for k,value in GALength_Path[headnode, tailnode].items():
			GANormal_Path_Length[headnode, tailnode][k] = ((Temp_Sum - value)/Normal_sum)*len(GALength_Path[headnode, tailnode].keys())
	    
	    #normalize ADTT
	    GANormal_Path_ADTT = {}
	    for headnode, tailnode in GAPath_ADTT.keys():
		GANormal_Path_ADTT[headnode, tailnode] = {}
		if len(GAPath_ADTT[headnode, tailnode].keys()) == 1:
		    GANormal_Path_ADTT[headnode, tailnode][1] = 1
		elif len(GAPath_ADTT[headnode, tailnode].keys()) > 1:
		    Temp_Sum = 0
		    for k,value in GAPath_ADTT[headnode, tailnode].items():
			Temp_Sum += value
		    for k,value in GAPath_ADTT[headnode, tailnode].items():
			GANormal_Path_ADTT[headnode, tailnode][k] = (value/Temp_Sum)*len(GAPath_ADTT[headnode, tailnode].keys())
	    
	    #shortest distance of node i with all emergency nodes
	    omega = {}  
	    for node in G.nodes:
		if node in G.emergnode:
		    omega[node] = 1
		else:
		    omega[node] = 0
		    
		    
	    for head, tail in GALength_Path.keys():
		if head in G.emergnode or tail in G.emergnode:
		    omega[head] = max(omega[head], 1/GALength_Path[head,tail][1])
		    omega[tail] = max(omega[tail], 1/GALength_Path[head,tail][1])
		    
	    #compute the weight of each node
	    GANodeWeight = {}
	    sumomega = sum(omega.values())
	    for node in G.nodes:
		GANodeWeight[node] = omega[node]/sumomega              
        
            R_G_x = RE.resilience_evaluation(G.nodes, GAL, GANormal_Path_Length,GAFresilience_Path, GANodeWeight, GANormal_Path_ADTT)
	   
	    Total_cost = 0
	    for headnode, tailnode in G.arcs:
		Total_cost += population[eachChromo][headnode, tailnode] * G.cost[headnode, tailnode]
	    
	    if Total_cost > 2*investment:
		Penalty_value = -1000000
	    else: Penalty_value = 0
		    
	    chromos_fitness[eachChromo] = R_G_x + Penalty_value
	    
		    
	    print Total_cost, chromos_fitness[eachChromo], sum(population[eachChromo].values())	    
               
        
    if GA_Construct_open == 1:  #construct new bridges 
        for eachChromo in population.keys():
            #add the new link into the network based on chromo
            print population[eachChromo]
            for (i,j) in population[eachChromo].keys():
                if (i,j) not in E_l and population[eachChromo][i,j] != 0:
                    E_l.append((i,j))
                    q_l[i,j] = 1
                if (i,j) in E_l and population[eachChromo][i,j] == 0:
                    E_l.remove((i,j))
                    del q_l[i,j]                
        E_comp = copy.deepcopy(E_l)
        q_comp = copy.deepcopy(q_l)
        ##print E_l
        #R_G_x = RE.resilience_evalueation(V_l, E_comp, u_l, q_comp)
        
        print "eachChromo",R_G_x
        E_comp = copy.deepcopy(E_l)
        q_comp = copy.deepcopy(q_l)        
        result = FE.friability_evaluation(V_l, E_comp, u_l, q_comp,  R_G_x)
        F_max_x = result[1]
        print "eachChromo",F_max_x
        
    
        
    return chromos_fitness

def select(population_fitness, cur_population, top):
    
    '''rank the fitness value of current population, update best_solution, best_fitness'''

    
    sorted_population = sorted(population_fitness.iteritems(), key=operator.itemgetter(1))
    length = len(sorted_population)
    selected_chromos = {}
    selected_chromo = []
    for i in xrange(1,top+1):
        chromo = sorted_population[length -i][0]
        selected_chromo.append(chromo)
    
    population_best_solution = copy.deepcopy(cur_population[selected_chromo[0]])
    populationbest_fitness = copy.copy(population_fitness[selected_chromo[0]])
        
    for i in selected_chromo:
        selected_chromos[i] = copy.deepcopy(cur_population[i])
        
    return selected_chromos, population_best_solution,  populationbest_fitness 
    

def generate_offspring(num_population, selected_population, crossover_rate, mutation_rate):
    '''Taking a ranked population return a new population by breeding the ranked one'''
    new_chromos = {}
    
    eachChromo = 0
    
    while eachChromo  <= num_population:
        ch1 = random.choice(selected_population.keys())
        ch2 = random.choice(selected_population.keys())
        new_chromos[eachChromo], new_chromos[eachChromo+1]  = copy.deepcopy(breed(selected_population[ch1],selected_population[ch2], crossover_rate, mutation_rate))
        eachChromo += 2
        
    return new_chromos

def breed(ch1, ch2, crossover_rate, mutation_rate):
    '''Using crossover and mutate it generates two new chromos from the selected pair'''
    
    #use crossover and mutation
    newch1, newch2 = {}, {}
    
    #remove the duplicated link index from BinVar, split binary variables to BinVar1 and BinVar2
    BinVar1,BinVar2 = [], []
    for (i,j) in ch1.keys():
        if (j,i) not in BinVar1:
            BinVar1.append((i,j))
        else:
            BinVar2.append((i,j))   
    
    chromo1, chromo2 = {}, {}
    for (i,j) in BinVar1:
        chromo1[i,j] = ch1[i,j]
        chromo2[i,j] = ch2[i,j]
        
    #all the cross, inerit, mutation is based on binvar1 and binvar2 is reversed i,j
    if random.random() < crossover_rate: # rate dependent crossover of selected chromosomes
        newch1, newch2 = crossover(chromo1, chromo2)
    else:
        newch1, newch2 = chromo1, chromo2  
    
    if random.random() < mutation_rate:
        newch1 = mutation(newch1)
    
    if random.random() < mutation_rate:
        newch2 = mutation(newch2)    
    
    #make sure the same link has same value (i,j) = (j,i)
    for (i,j) in BinVar1:
        newch1[j,i] = newch1[i,j]
        newch2[j,i] = newch2[i,j]
        
    return newch1, newch2


def crossover(chromo1, chromo2):
    '''crossover two pairs chromos'''
    #sorted the two choromos and save as dictionary
    sorted1 = sorted(chromo1.iteritems(), key=operator.itemgetter(0))
    sorted2 = sorted(chromo2.iteritems(), key=operator.itemgetter(0))
    
    #one point crossover
    pt = random.randint(0,len(sorted1)-1)
    offspring1 = sorted1[:pt] + sorted2[pt:]
    offspring2 = sorted2[:pt] + sorted1[pt:]
    
    newchromo1, newchromo2 = {}, {}
    for element in offspring1:
        newchromo1[element[0][0],element[0][1]] = element[1]
        
    for element in offspring2:
        newchromo2[element[0][0],element[0][1]] = element[1] 
        
    return newchromo1, newchromo2

def mutation(chromo):
    
    #convert dictionary to list
    sorted_chromo = sorted(chromo.iteritems(), key=operator.itemgetter(0))
    
    #exchange mutation
    position1 = random.randint(0, len(sorted_chromo)-1 )
    position2 = random.randint(0, len(sorted_chromo)-1 )
    sorted_chromo[position1], sorted_chromo[position2] = sorted_chromo[position2], sorted_chromo[position1]    
    
    #convert list ot dictionary
    newchromo = {}
    for element in sorted_chromo:
        newchromo[element[0][0],element[0][1]] = element[1]

    return newchromo



def main(node_list,edge_list, BinVar, num_population,max_iteration, max_time, crossover_rate, mutation_rate, top,  seed, investment, GA_Reinfoce_open, GA_Construct_open, G, sampleid):
    
    

    
    random.seed(seed)
    
    init_population = generate_population(BinVar, num_population, investment)
    
    cur_population = copy.deepcopy(init_population)
    
    iteration = 0 
    start_time = time.clock()
    run_time = 0
    
    best_solution = {}               #global variable, best solution
    best_fitness =  -float("inf")     #global variable, best fitness socre found
    
    #investment = 6
    
    g = open('GA_details_{}_{}_{}_{}.txt'.format(sampleid, num_population,max_iteration,seed),"w")
    g.close()
    
    terminal  = 0
   
    
    while iteration <= max_iteration and run_time <= max_time:
        
        local_V = copy.deepcopy(node_list)
        local_E = copy.deepcopy(edge_list)
        
        
        population_fitness = fitness_evaluate(cur_population, local_V, local_E, investment, GA_Reinfoce_open, GA_Construct_open, G)    #compute the fitness value of current population
        
        selected_population, pop_best_solution, pop_best_fitness = select(population_fitness, cur_population, top)   #select the top chromos in current population and generate offsprint
        
        previous_best = best_fitness
         
        #update the best so far solution
        if pop_best_fitness > best_fitness:
            best_fitness = pop_best_fitness
            best_solution = copy.deepcopy(pop_best_solution)
        
        #terminal criterion    
        if previous_best == best_fitness:
            terminal  += 1
        else:
            terminal  = 0
        
        if terminal >= max_iteration/10:
            break
        
        g = open('GA_details_{}_{}_{}_{}.txt'.format(sampleid, num_population,max_iteration,seed),"a")
        g.write('{},{},{},{}\n'.format(best_fitness, iteration, run_time, best_solution ))
        g.close()
        
        #offspring
        offspring_population = generate_offspring(num_population, selected_population, crossover_rate, mutation_rate)
        
        #update the best so far solution
        
        iteration += 1
        run_time = time.clock() - start_time
        
        
        
    return iteration, run_time, best_fitness, best_solution
    

