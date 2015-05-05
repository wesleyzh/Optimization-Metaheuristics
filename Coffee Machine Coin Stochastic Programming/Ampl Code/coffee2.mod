param nCUT >= 0 integer;
param cut_type {1..nCUT} symbolic within {"point","ray"};param lambda_c {SCENARIO_c, SCENARIO_m, 1..nCUT};param lambda_m {SCENARIO_c, SCENARIO_m, 1..nCUT};param u := 110;param c := 15;
var x >= 0, <=u;var z;
minimize Total_Cost:c*x + z;
subj to Cut_Defn {k in 1..nCUT}:if cut_type[k] = "point" then z >= sum {i in SCENARIO_c, j in SCENARIO_m}lambda_c[i,j,k]*(t_c*d_c[i]-x) +sum {i in SCENARIO_c, j in SCENARIO_m} lambda_m[i,j,k]*(t_m*d_m[j]- x);