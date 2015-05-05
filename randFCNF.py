#Code to generator random feasible fixed-charge network flow instances
#each network is created based on the following input:

#    numNodes = number of nodes
#    S = sparse value (randomly generated, but can be set)

#    k commodities

#    R requirements for each node and commodity   
#      %s = %supply nodes; %d = %demand nodes  
#      minR, maxR = minimum and maximum requirements

#    c variable costs on each arc       
#      minC, maxC = minimum and maximum costs

#    f fixed costs on each arc
#      minF, maxF = minimum and maximum costs

#    M capacity for each commodity on each arc -- for uncapacitated arcs, this is set to total supply in network



import random
from networkx import *
import matplotlib.pyplot as plt
from gurobipy import *
from pygraphviz import *
import math


def FCNFgenerator(seed, m, n,supplyPct, demandPct, rhsMin, rhsMax, cMin, cMax, fMin, fMax, K, arcs, Sparse = -1):
                       
        random.seed(seed)          
        #user input -----------------------------------------------------------------
        
        #nodes 
        numNodes=n
        
        #commodities
        numCommodities = K
        
        #set min and max on absolute value of node requirements (rhs)
        rhs_min = rhsMin
        rhs_max = rhsMax
        sPct = supplyPct         #percent of nodes that are supply nodes
        dPct = demandPct         #percent of nodes that are demand nodes
        
        if sPct + dPct > 1:
                print "\nUser Error: Supply + Demand Percentages exceed 100%\n"
                exit(1)
        
        #set min and max on variable (c) and fixed costs (f)
        c_min = cMin 
        c_max = cMax
        f_min = fMin
        f_max = fMax
        
        if cMax < cMin:
                print "\nUser Error: min varcost < max varcost\n"
                exit(1)
                
        if fMax < fMin:
                print "\nUser Error: min fixedcost < max fixedcost\n"
                exit(1)
        
        #begin automatic feasible FCNF creation................................
        
        nodes = range(0,numNodes)
        commodities = range(0,numCommodities)
        #arcs = []
        
        if Sparse == -1:
                S = random.randint(numNodes-1, (numNodes*(numNodes-1))/2)      #divided by two since essentially each undirected edge will be converted to two directed edges 
        else:
                if Sparse > numNodes-1 and Sparse <= numNodes*(numNodes-1)/2:
                        S = Sparse
                else:
                        print "User Error: Sparse value is outside of bounds: ({},{}), Sparse={}".format(numNodes-1,numNodes*(numNodes-1)/2,Sparse)
                        exit(1)
        
        e = 0
        #create connected graph ----------------------------------------
        for i in range(numNodes-1):
                prevNode=random.randint(0,i)
                arcs.append((prevNode,i+1))
                arcs.append((i+1,prevNode))
                   
        
        complete=[]
        for i in range(numNodes-1):
                for j in range(i+1,numNodes):
                        complete.append((i,j))
        
        missing = set(complete) - set(arcs)
        
        if len(missing) >= S-int(len(arcs)/2):
                toAdd = random.sample(missing, S-int(len(arcs)/2))
        
                for i,j in toAdd:
                        arcs.append((i,j))
                        arcs.append((j,i))                
        #end create connected graph ----------------------------------
                 
                        
        # begin distribution of supply and demand -------------                  
        requirements = {}           
        demandNodes={}
        supplyNodes={}
        totSupply = {}  
        totDemand = {}
        
        for k in commodities:
                totSupply[k] = 0
                totDemand[k] = 0
                demandNodes[k]=[]
                supplyNodes[k]=[]        
                
        for k in commodities:
                supplyCnt = 0
                demandCnt = 0
                
                condition = True
                while condition:                       
                        for i in nodes:    
                                requirements[i,k] = 0
                                if random.random() < sPct:
                                        requirements[i,k] = round(random.uniform(rhs_min, rhs_max))
                                        totSupply[k] = totSupply[k] + requirements[i,k]
                                        supplyNodes[k].append(i)
                                        supplyCnt = supplyCnt + 1
                                elif random.random() < dPct + sPct:
                                        demandNodes[k].append(i)
                                        demandCnt = demandCnt + 1
                                        
                        if len(nodes) > len(supplyNodes[k]):
                                condition = False
                        else:
                                totSupply[k] = 0
                                supplyCnt = 0
                                demandCnt = 0
                                demandNodes[k]=[]                       
                                supplyNodes[k]=[]
                                                           
                if supplyCnt == 0:
                        s = random.choice(nodes)
                        requirements[s,k] = round(random.uniform(rhs_min, rhs_max))
                        totSupply[k] = totSupply[k] + requirements[s,k]
                        supplyNodes[k].append(s)    
                        if s in demandNodes[k]:
                                demandNodes[k].remove(s)
                                demandCnt = demandCnt - 1
                        
                if demandCnt == 0:
                        
                        d = random.choice(nodes)
                        while d in supplyNodes[k]:
                                d = random.choice(nodes)
                        
                        demandNodes[k].append(d)
                        demandCnt = demandCnt + 1        
                        requirements[d,k] = -totSupply[k]
                        totDemand[k] = totDemand[k] - requirements[d,k]
        
                else:
                        for i in demandNodes[k]:
                                if totDemand[k] >= totSupply[k]:
                                        break
                                requirements[i,k] = -1*round(sPct/dPct * random.uniform(rhs_min, rhs_max))
                                totDemand[k] = totDemand[k] - requirements[i,k]
        
                #dif = math.ceil((totSupply[k] - totDemand[k])/len(demandNodes[k]))
                dif = (totSupply[k] - totDemand[k])/len(demandNodes[k])
                if dif > 0: 
                        dif = math.ceil((totSupply[k] - totDemand[k])/len(demandNodes[k]))
                if dif < 0: 
                        dif = math.floor((totSupply[k] - totDemand[k])/len(demandNodes[k]))                
                
                if dif <> 0:
                        for i in demandNodes[k]:
                                requirements[i,k] = requirements[i,k] - dif
                                             
                        dif = quicksum(requirements[i,k] for i in nodes)
                        
                        j = random.choice(demandNodes[k])
                        requirements[j,k]=requirements[j,k] - dif
                        
                totDemand[k] = 0
                totSupply[k] = 0
                for i in nodes:
                        if requirements[i,k] > 0:
                                totSupply[k] += requirements[i,k] 
                        elif requirements [i,k] < 0:
                                totDemand[k] -= requirements[i,k] 
                
                if totDemand[k] - totSupply[k] <> 0:
                        print 'User Error: Supply does not meet demand for commodity {}'.format(k)
                        exit(1)       
        #end distribution of supply and demand -----------
                             
                                             
        #begin costs, model variables, model constraints --------------                                  
        varcost = {}
        fixedcost = {}
        
        arcs = tuplelist(arcs)
        
        karcs = []
        for k in commodities:
                for i,j in arcs:
                        karcs.append((i,j,k))
                
        karcs = tuplelist(karcs)
        
        for i,j in arcs:
                fixedcost[i,j] = random.uniform(f_min, f_max)     #randomly generate fixed costs
                
                for k in commodities:
                        varcost[i,j,k] = random.uniform(c_min, c_max)       #randomly generate variable costs
           
           
        flow={}
        decision={}   
                
        for i,j in arcs:
                for k in commodities:
                        flow[i,j,k] = m.addVar(name='flow_%s_%s_%s' % (i, j, k), obj=varcost[i,j,k], lb = 0)             #create flow variables (per arc, per commodity)
                
                decision[i,j] = m.addVar(vtype = GRB.BINARY, obj=fixedcost[i,j], name='decision_%s_%s' % (i,j) , lb = 0, ub = 1)  #binary decision vars (per arc)            
        
        m.update()
        
        #add flow-balance constraints -----
        for k in commodities:
                for j in nodes:
                        m.addConstr(
                                quicksum(flow[a,b,c] for a,b,c in karcs.select('*',j,k)) +
                                requirements[j,k] ==                                       
                                quicksum(flow[a,b,c] for a,b,c in karcs.select(j,'*',k)),'node_%s_%s' % (j,k))    
                      
        #add Big-M constraints  
        for i,j,k in karcs:
                m.addConstr(flow[i,j,k] <= totSupply[k]*decision[i,j],'BigM_%s_%s_%s' % (i, j, k))            #Big-M constraints
                
        m.update()
        
        FCNFresult = [requirements, flow, varcost, fixedcost, totSupply]
        return FCNFresult
        
        
        
        
        
        

   

            
         