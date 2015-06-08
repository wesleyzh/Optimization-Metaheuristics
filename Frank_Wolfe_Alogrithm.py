"""
The Frank-Wolfe Alogrithm for nonlinear programming
reference: http://ssdi.di.fct.unl.pt/mq/Docs/MaterialApoio/OR%20Tutor/np/fw/page1.html

Problem requirements:
- the objective function is nonlinear
- all constraints are linear

Input:
nonlinear programming model

Output:
optimal solution


"""


from sympy import symbols, diff, Eq, solve, expand 
from gurobipy import *
from scipy.optimize import fsolve
import copy

#create the problem


x1, x2 = symbols('x1 x2', real=True)  #variables
x_list = [x1, x2]

f = 32 * x1 - 1 * x1 ** 4 + 8 * x2 - 1 * x2 ** 2  #objective function

#contstraints

m = Model("NLP")
m.ModelSense = -1  #maximize problem
m.setParam( 'OutputFlag', 0) 
m.setParam( 'LogToConsole', 0 )
m.setParam( 'LogFile', "" )   

X = [x1, x2]
x = {}

for i in X:
    x[i] = m.addVar(lb=0, name="x_{}".format(i))
    
m.update()
    
#linear constratints
constratains = {}

m.addConstr(x[x1] - x[x2] <= 1)
m.addConstr(3*x[x1] + x[x2] <= 7)

m.update()


cur_solution = {x1: 0, x2: 0}  #initial solution
flag = True
iter = 0

while flag:
    
    print "Iteration ", iter
    print cur_solution
    iter += 1
    
    m.reset()
    
    prve_solution = copy.copy(cur_solution)

    df = {}
    df[x1] = diff(f, x1).subs(prve_solution)
    df[x2] = diff(f, x2).subs(prve_solution)
    
    for i in X:
        x[i].obj = df[i]
        
    m.update()
    
    try:
        m.optimize()
        
        if m.status == 2:
            cur_solution = m.getAttr('x', x)
            
            
    except GurobiError:
        print GurobiError
        
    t = symbols("t", real=True)
    
    #segment between previous solution and currnet solution
    segment = {}
    
    for i in X:
        segment[i] = prve_solution[i]+t*(cur_solution[i] - prve_solution[i])
        
    #update objective function with t
    h = 32 * segment[x1] - (segment[x1]) ** 4 + 8 * segment[x2] - segment[x2] ** 2
    h = expand(h)
    dh = diff(h, t)
    eqn = Eq(dh, 0)
    t_solution = solve(eqn)[0]
    
    if t_solution <= 1 and t_solution >= 0:
        t_candidate = [t_solution, 1]
        best_h = h.subs({t: 0})
        best_t = 0
        for i in t_candidate:
            if h.subs({t: i}) > best_h:
                best_t = i
    else:
        t_candidate = [1]
        best_h = h.subs({t: 0})
        best_t = 0
        for i in t_candidate:
            if h.subs({t: i}) > best_h:
                best_t = i    
    
    #get new solution
    
    for i in X:
        cur_solution[i] = segment[i].subs({t: best_t})
        
    flag = False
    
    for key in prve_solution.keys():
        if abs(prve_solution[key] - cur_solution[key]) > 0.001:
            flag = True
        
            
    pass


print "\nOptimal Solution"            
print f.subs(cur_solution)
print cur_solution
