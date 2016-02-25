# Vertex_Cover

Solving the vertex cover problem using the branch and bound strategy. 

Instruction for running branch-and-bound algorithm

Input: -inst <filename.graph>, -alg[BnB|Approx|LS1|LS2],
           -time <cutoff in seconds>, -seed <random seet>
           where the -seed argument can be omitted for Bnb and Approx
Output: trace file and sol file: note the output files will be put in 
        a subdirectory named output. 

For example: to run it for the email.graph file with branch and bound
             with 30s as cutoff time: type in
             python vertex_cover.py -inst ./DATA/email.graph -alg BnB -time 30

where ./DATA/email.graph is the path to the graph file.


The core algorithm of branch and bound is in the branch_and_bound.py file. 
