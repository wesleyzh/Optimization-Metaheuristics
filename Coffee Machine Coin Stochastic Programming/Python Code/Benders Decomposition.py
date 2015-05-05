'''
********************************************************
* The model shows a Benders Decomposition for a stochasitic programming coffee machine management problem.*

* The original MIP is decomposed into two problems.                           *

* The subproblem is using the dual formulation.            			*

* For consistency, this is built using an equivalent AMPL model coffee.run    *

#********************************************************
'''


from gurobipy import *
#from pygraphviz import *
#import math
from decimal import *
import copy
import random
import numpy as np
import sys

class Coffee_machine_management:
    
    def __init__(self, Num_scenoria, coins_for_coffee, coins_for_milk, cost_of_leave, cost_of_missing, capacity):
        self.S = Num_scenoria
        self.SENARIO_c = range(1, self.S+1)
        self.SENARIO_m = range(1, self.S+1)
        self.d_c = {}   #stochastic demand of coffee 
        self.d_m = {}  #stochastic demand of milk
        self.p_c = {}  #probability of coffee
        self.p_m = {}  #probability of milk
        self.t_c = coins_for_coffee
        self.t_m = coins_for_milk
        self.c = cost_of_leave  #cost of leaving the coins in the box is c euros per each deposited euro
        self.q = cost_of_missing  #cost of q for each euro missing the coin box
        self.u = capacity  #capacity of the coin box
        
        self.sm = Model('SubProblem')
        self.sm.setParam( 'OutputFlag', 0 ) 
        self.sm.setParam( 'LogToConsole', 0 )
        self.sm.setParam( 'LogFile', "" )   
        self.sm.params.threads = 1
        self.sm.params.NodefileStart = 0.5
        self.sm.params.timeLimit = 1800
        self.sm.params.DualReductions = 0   #turn off to avoid the optimization status of INF_OR_UNBD
        self.sm.params.InfUnbdInfo = 1  #Additional info for infeasible/unbounded models
        self.sm.ModelSense = -1  #sub problem is a maximization problem
        
        
        self.mm = Model('MasterProblem')
        self.mm.setParam( 'OutputFlag', 0 ) 
        self.mm.setParam( 'LogToConsole', 0 )
        self.mm.setParam( 'LogFile', "" )   
        self.mm.params.threads = 1
        self.mm.params.NodefileStart = 0.5
        self.mm.params.timeLimit = 1800
        self.mm.params.DualReductions = 0   #turn off to avoid the optimization status of INF_OR_UNBD
        self.mm.params.InfUnbdInfo = 1  #Additional info for infeasible/unbounded models
        
    def Sub_problem(self, X):
        
        #Generate the sub problem dual problem
        
        self.lambda_c = {}
        self.lambda_m = {}
        
        self.sm.reset()
        for v in self.sm.getVars():
            self.sm.remove(v)
        for c in self.sm.getConstrs():
            self.sm.remove(c)        
          
        for i in self.SENARIO_c:
            for j in self.SENARIO_m:
                self.lambda_c[i,j] = self.sm.addVar(name='lambda_c_%s_%s' % (i, j), obj = self.t_c*self.d_c[i]-X, lb = 0)
                self.lambda_m[i,j] = self.sm.addVar(name='lambda_m_%s_%s' % (i, j), obj = self.t_m*self.d_m[j]-X, lb = 0)
                
        self.sm.update()
        
        for i in self.SENARIO_c:
            for j in self.SENARIO_m:
                self.sm.addConstr(self.lambda_c[i,j] <= self.p_c[i]*self.p_m[j]*self.q)
                self.sm.addConstr(self.lambda_m[i,j] <= self.p_c[i]*self.p_m[j]*self.q)
                
        self.sm.update()
        

    def Master_problem(self, nCut, cut_type, lambda_c_k, lambda_m_k, c_m_k):
    
        #Generate the Master Problem
        self.mm.reset()
        for v in self.mm.getVars():
            self.mm.remove(v)
        for c in self.mm.getConstrs():
            self.mm.remove(c)       
        
        self.x = self.mm.addVar(name='amount', obj = self.c, lb=0, ub=self.u)
        self.z = self.mm.addVar(name ='z', obj = 1)
        
        self.mm.update()

        for k in range(1, nCut+1):
            if cut_type[k] == "point":
                self.mm.addConstr(self.z >= quicksum(lambda_c_k[a, b, k]*(self.t_c*self.d_c[a]-self.x) for a, b, k in c_m_k.select('*', '*', k))+
                                  quicksum(lambda_m_k[a, b, k]*(self.t_m*self.d_m[b]-self.x) for a, b, k in c_m_k.select('*', '*', k)))
                
        self.mm.update()


def Benders_decomposition():
    
    Num_scenoria, coins_for_coffee, coins_for_milk, cost_of_leave, cost_of_missing, capacity = 3, 2, 1.5, 15, 9, 110
        
    CMMP = Coffee_machine_management(Num_scenoria, coins_for_coffee, coins_for_milk, cost_of_leave, cost_of_missing, capacity)
    
    #assign parameters
    CMMP.d_c[1] = 40
    CMMP.d_c[2] = 80
    CMMP.d_c[3] = 120
    
    CMMP.d_m[1] = 30
    CMMP.d_m[2] = 80
    CMMP.d_m[3] = 120
    
    CMMP.p_c[1] = 0.25
    CMMP.p_c[2] = 0.5
    CMMP.p_c[3] = 0.25
    
    CMMP.p_m[1] = 0.25
    CMMP.p_m[2] = 0.5
    CMMP.p_m[3] = 0.25    
    
    #initialization
    nCut = 0
    z = 0
    X = 1
    gap = float('inf')
    
    cut_type = {}
    
    lambda_c = {}
    lambda_m = {}
    lambda_c_k = {}
    lambda_m_k = {}
    
     
    
    #Benders decomposition procedure
    
    while True:
        
        print "\n Iteration %s" % (nCut + 1)
        #create subproblems
        CMMP.Sub_problem(X)           
        
        try:
            
            CMMP.sm.optimize()
            
            
            if CMMP.sm.status == 5:
                print "Unbounded"
                nCut += 1
                cut_type[nCut] = "ray"
                
                for i in CMMP.SENARIO_c:
                    for j in CMMP.SENARIO_m:
                        lambda_c[i, j] = CMMP.sm.getVarByName('lambda_c_%s_%s' % (i, j))
                        lambda_m[i, j] = CMMP.sm.getVarByName('lambda_m_%s_%s' % (i, j))
                        
                #get the unboundedness direction of the variable and add cuts
                for i in CMMP.SENARIO_c:
                    for j in CMMP.SENARIO_m:                
                        lambda_c_k[i, j, nCut] = lambda_c[i, j].UnbdRay #CMMP.sm.getAttr('UnbdRay', lambda_c[i, j])
                        lambda_m_k[i, j, nCut] = lambda_m[i, j].UnbdRay#CMMP.sm.getAttr('UnbdRay', lambda_m[i, j])
                        
            elif CMMP.sm.status == 2 or CMMP.sm.status == 9:
                dual_cost = CMMP.sm.ObjVal
                gap = min(gap, dual_cost - z)
                
                print dual_cost, z
                
                if dual_cost <= z + 0.00001:
                    break
                
                nCut += 1
                cut_type[nCut] = "point"
            
                for i in CMMP.SENARIO_c:
                    for j in CMMP.SENARIO_m:
                        lambda_c[i, j] = CMMP.sm.getVarByName('lambda_c_%s_%s' % (i, j))
                        lambda_m[i, j] = CMMP.sm.getVarByName('lambda_m_%s_%s' % (i, j))
            
                #get the unboundedness direction of the variable and add cuts
                for i in CMMP.SENARIO_c:
                    for j in CMMP.SENARIO_m:                
                        lambda_c_k[i, j, nCut] =  lambda_c[i, j].x #CMMP.sm.getAttr('x', lambda_c[i, j])
                        lambda_m_k[i, j, nCut] =  lambda_m[i, j].x #CMMP.sm.getAttr('x', lambda_m[i, j])                
                
            
        except:
            print "Sub problem solve error"
            break
        
        print "Re-solve Master Problem"
        
        c_m_k = []
        for i in CMMP.SENARIO_c:
            for j in CMMP.SENARIO_m:
                for k in range(1, nCut+1):
                    c_m_k.append((i, j, k))
                        
        c_m_k = tuplelist(c_m_k)
            
        #create master roblems
        CMMP.Master_problem(nCut, cut_type, lambda_c_k, lambda_m_k, c_m_k)           
        
        try:
            
            CMMP.mm.optimize()
            
            x = CMMP.mm.getVarByName('amount').x
            z = CMMP.mm.getVarByName('z').x
            
            X = x
            
            
        except:
            print "Master problem error"
            break
            
        
    print x    
        

if __name__ == '__main__':
    
    Benders_decomposition()
    
    
    
    