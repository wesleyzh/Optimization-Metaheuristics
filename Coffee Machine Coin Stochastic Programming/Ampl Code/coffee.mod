#This is the original problem

set SCENARIOS_c := 1 2 3;
set SCENARIOS_m := 1 2 3;

param d_c {SCENARIOS_c};
param d_m {SCENARIOS_m};
param p_c {SCENARIOS_c};
param p_m {SCENARIOS_m};
param c := 15;
param q := 10;
param u := 110;
param t_c := 2;
param t_m := 1.5;

var x >= 0, <= 110;
var y_c {SCENARIOS_c, SCENARIOS_m} >= 0;
var y_m {SCENARIOS_c, SCENARIOS_m} >= 0;

minimize Total_Cost:
x*c + sum{i in SCENARIOS_c, j in SCENARIOS_m}  p_c[i]* p_m[j]*q*(y_c[i,j]+
y_m[i,j]);

subj to Demand_c {i in SCENARIOS_c, j in SCENARIOS_m}:
x + y_c[i,j] >= t_c*d_c[i];

subj to Demand_m {i in SCENARIOS_c, j in SCENARIOS_m}:
x + y_m[i,j] >= t_m*d_m[j];
