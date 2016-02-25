# this file implements the approximation algorithm

import networkx as nx
import time
from graph_io import read_graph
import os
import os.path

class approximation:

    def edge_deletion(self, G):
        """implementation of the edge delection approximation algorithm (the algorithm
           that is dicussed in class)
           input: a networkx graph object G
           output: a list of vertices that form a vertex cover"""
        cover = set()
        covered_edges = set()

        for u, v in G.edges_iter():
            # if edge (u, v) is not covered, add u and v to the cover
            #  and add all the edges that are adjacent to u or v to covered_edges
            if (u, v) not in covered_edges and (v, u) not in covered_edges:
                cover.add(u)
                cover.add(v)
                covered_edges = covered_edges | set(G.edges([u, v]))

        return list(cover)

    def edge_delection_with_cutoff(self, G, cutoff_time, trace_file, result_file):
        """same implementation as edge_deletion(), but with cutoff_time, trace_file,
           and result_file arguments, used as a standalone function to generate results"""
        cover = set()
        covered_edges = set()

        unfinished = False
        start_time = time.time()

        for u, v in G.edges_iter():

            if (u, v) not in covered_edges and (v, u) not in covered_edges:
                cover.add(u)
                cover.add(v)
                covered_edges = covered_edges | set(G.edges([u, v]))
                # if reaches the cutoff_time before finding a solution, mark as unfinished
                if time.time() - start_time > cutoff_time:
                    unfinished = True
                    break

        if unfinished:
            cover = set()

        cover = sorted(list(cover))

        output_trace = open(trace_file, 'w')
        current_time = time.time() - start_time
        output_trace.write("%.2f,%d\n" %(current_time, len(cover)))
        output_trace.close()

        output_result = open(result_file, 'w')
        output_result.write("%d\n" % (len(cover)) )
        if len(cover) > 0:
            for i in range(len(cover)-1):
                output_result.write("%d," % (cover[i]))
            output_result.write("%d" % (cover[-1]))
        output_result.close()

        return cover

def run_approx(input_file, cutoff_time):
    """interface file to the convenience
    input: input_file(the graph file), current_time
    output: none.
    side effect: save trace file and output file to the output folder"""

    approx_solver = approximation()

    # extract the filename without surfix
    start = input_file.rfind("/")
    end = input_file.find(".graph")
    filename = input_file[start+1:end]

    # generate output file names
    output_sol = "./output/" + filename + "_Approx_" + str(cutoff_time) + ".sol"
    output_trace = "./output/" + filename + "_Approx_" + str(cutoff_time) + ".trace"

    # output files are put in the "output" folder, if this folder doesn't exist,
    #  create the folder
    try:
        os.makedirs("./output")
    except OSError:
        if not os.path.isdir("./output"):
            raise

    # read in the graph
    G = read_graph(input_file)
    approx_solver.edge_delection_with_cutoff(G, cutoff_time, output_trace, output_sol)



if __name__ == '__main__':
    run_approx("./DATA/email.graph", 10)
