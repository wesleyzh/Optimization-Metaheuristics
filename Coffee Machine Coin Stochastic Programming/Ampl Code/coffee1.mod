param S := 3;
set SCENARIO_c := 1..S;set SCENARIO_m := 1..S;
param X;param d_c {SCENARIO_c};param d_m {SCENARIO_m};param p_c {SCENARIO_c};param p_m {SCENARIO_m};

param t_c := 2;param t_m := 1.5;param q := 9;
var Lambda_c {SCENARIO_c, SCENARIO_m} >= 0;var Lambda_m {SCENARIO_c, SCENARIO_m} >= 0;
maximize Dual_Cost:       sum {i in SCENARIO_c, j in SCENARIO_m} Lambda_c[i,j]*(t_c*d_c[i]-X) +sum {i in SCENARIO_c, j in SCENARIO_m} Lambda_m[i,j]*(t_m*d_m[j]- X);subj to Dual_c {i in SCENARIO_c, j in SCENARIO_m}:       Lambda_c[i,j] <= p_c[i]*p_m[j]*q;subj to Dual_m {i in SCENARIO_c, j in SCENARIO_m}:       Lambda_m[i,j] <= p_c[i]*p_m[j]*q;