""" Wrapper file for the 4 algorithms,
    Input: -inst <filename.graph>, -alg[BnB|Approx|LS1|LS2],
           -time <cutoff in seconds>, -seed <random seet>
           where the -seed argument can be omitted for Bnb and Approx
    Output: trace file and sol file
    For example: to run it for the email.graph file with branch-and-bound
                 with 30s as cutoff time: type in
                 python vertex_cover.py -inst ./DATA/email.graph -alg BnB -time 30
"""

import sys
import branch_and_bound
import approximation
import argparse

def main():

    parser = argparse.ArgumentParser(description="arguments")
    parser.add_argument('-inst', help='path to input graph', required = True)
    parser.add_argument('-alg', help='algorithm choice[BnB|Approx|LS1|LS2]', required = True)
    parser.add_argument('-time', help='cutoff time in seconds', required = True)
    parser.add_argument('-seed', help='seed', required = False)

    args = parser.parse_args()
    input_graph = args.inst
    algs = args.alg
    cutoff_time = int(args.time)
    if args.seed != None:
        seed = int(args.seed)


    if algs == "BnB":
        branch_and_bound.run_bnb(input_graph, cutoff_time)
    else:
        if algs == "Approx":
            approximation.run_approx(input_graph, cutoff_time)
        else:
            if algs == "LS1":
                pass # replace this line with a call to LS1
            else:
                if algs == "LS2":
                    pass # replace this line with a call to LS2
                else:
                    print "error: please choose among [BnB|Approx|LS1|LS2]"
                    exit(1)

if __name__ == '__main__':
    main()
