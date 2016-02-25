# implementation of branch_and_bound algorithm

import networkx as nx
import approximation as approx
from priorityQueue import indexMinPQ
import operator
import time
from graph_io import read_graph
import cProfile
import os
import os.path


class bnb:

    def intersection(self, a, b):
        """compute intersection of two list, doesn't preserve order"""
        return list(set(a) & set(b))

    def lower_bound_edge_deletion(self, H):
        """return the lower bound of min-vc for graph H, using edge delection algorithm"""
        solver = approx.approximation()
        return len(solver.edge_deletion(H))/2

    def lower_bound_max_matching(self, H):
        """return the lower bound of min-vc for graph H, using max matching algorithm.
        Recall in a graph H, any matching as size less than or equal to any vc,
        so |max matching| <= |min-vc|. In particular, in a bipartite graph, "=" is
        attained. This uses networkx.max_weight_matching, which uses Edmonds' algorithm"""

        # divided by 2 since nx.max_weight_matching() returns a dict
        #  which repeats every edge in M  twice.
        return len(nx.max_weight_matching(H))/2


    def approx_edge_delection(self, H):
        """return the approx vc using the edge delection algorithm"""
        solver = approx.approximation()
        return solver.edge_deletion(H)

    def max_degree_vertex(self, G, sub_V):
        """return the max degree vertex among the vertices in sub_V in graph G"""
        if not set(sub_V) <= set(G.nodes()):
            raise KeyError("max_degree_vertex(): vertices are not all in the graph")
            return None
        vertex_degree_dict = nx.degree(G, sub_V)
        return max(vertex_degree_dict.iteritems(), key = operator.itemgetter(1))[0]

    def residual_graph(self, G, removal_V):
        """return the residual graph after removing all the vertices in the removal_V
        list, and all the vertices whose neighbor are all in removal_V"""
        if not isinstance(removal_V, list):
            removal_V = [removal_V]
        return [ v for v in G.nodes() if (v not in removal_V
                                 and not set(G.neighbors(v)) < set(removal_V)) ]

    def isCover(self, sub_V, G):
        """return True if sub_V is a vertex cover for G"""
        for e in G.edges_iter():
            if e[0] not in sub_V and e[1] not in sub_V:
                return False
        return True

    def still_is_cover(self, node, sub_V, G):
        is_cover = True
        neighbors = set(G.neighbors(node))
        if len(neighbors) > 0 and not neighbors <= set(sub_V):
            is_cover = False
        return is_cover

    def bnb_edge_delection(self, G, cutoff_time, trace_file, result_file, update_rate_0 = 10):
        """compute the min-vc using branch and bound
           input: G - a networkx Graph object,
                  cutoff_time: cutoff_time in seconds
                  trace_file: the trace file name
                  result_file: the result file name
                  update_rate_0: a parameter that controls
                                 how frequently we recompute lower bounds
           output: a tuple: (size_of_min_vc, min_vc),
                   size_of_min_vc is an integer
                   min_vc is a list of vertices
           side effects: save trace_file and result_file"""

        output_trace = open(trace_file, 'w')
        start_time = time.time()

        # if the graph is large (with more than 10000 nodes), we dynamically adjust
        #  the update rate
        if G.number_of_nodes() > 10000:
            update_rate_0 = G.number_of_nodes()/500
        if update_rate_0== 0:
            update_rate_0 = 1

        sub_problems = indexMinPQ()
        #initial_lb = self.lower_bound_edge_deletion(G)
        approx_solution = self.approx_edge_delection(G)
        initial_lb = len(approx_solution)/2
        sub_problems.push( (None, tuple(G.nodes()), tuple(G.nodes()), initial_lb),
                            G.number_of_edges())

        # update the current_best to the approx solution
        current_best = (len(approx_solution), approx_solution)

        # output one trace line
        current_time = time.time() - start_time
        output_trace.write("%.2f,%d\n" %(current_time, current_best[0]))

        counter = 0

        while not sub_problems.isEmpty():
            sub_p = sub_problems.pop()

            if sub_p[0] is None:
                sub_cover = []
            else:
                sub_cover = list(sub_p[0])                      # C in the pseudocode
            available_vertices = list(sub_p[1])                 # A in the pseudocode
            remaining_graph = G.subgraph(list(sub_p[2]))        # G' in the pseudocode
            current_lb = sub_p[3]

            if current_lb >= current_best[0]:
                pass
            if len(sub_p[2]) < 500:
                update_rate = 1
            else:
                update_rate = update_rate_0

            max_degree_v = self.max_degree_vertex(remaining_graph, available_vertices) # v in the pseudocode

            # the first expansion: add v to the partial cover
            cover_add_v = list(sub_cover)
            cover_add_v.append(max_degree_v)   # C_1 = C \union v
            new_residual_vertices = self.residual_graph(remaining_graph, max_degree_v)  # V'_1
            new_available_vertices = self.intersection(new_residual_vertices, available_vertices)  # A'_1 = A \cap V'_1
            new_residual_graph = G.subgraph(new_residual_vertices)

            if nx.number_of_edges( new_residual_graph ) == 0:       # cover_add_v is a vc
                if len(cover_add_v) < current_best[0]:              # update the current_best
                    current_best = (len(cover_add_v), cover_add_v)

                    current_time = time.time() - start_time
                    output_trace.write("%.2f,%d\n" %(current_time, current_best[0]))

            elif len(new_available_vertices) > 0:                  # check it is not dead end
                # only recompute the lower bound every update_rate steps
                #  otherwise, we just use the previous lower bound (note this is still
                #    a lower bound, although it may not be as tight at the recomputed lb)
                if counter % update_rate == 0:
                    lb = len(cover_add_v) + self.lower_bound_edge_deletion(new_residual_graph)
                    counter = 0
                else:
                    lb = current_lb
                counter += 1
                if lb < current_best[0]:                           # add to the subproblems queue
                    sub_problems.push((tuple(cover_add_v), tuple(new_available_vertices),
                                       tuple(new_residual_vertices), lb),
                                       new_residual_graph.number_of_edges())

            # the second expansion: mark v as not selected
            cover_unselect_v = list(sub_cover)
            available_vertices_delete_v = list(available_vertices)
            available_vertices_delete_v.remove(max_degree_v)

            # cover_unselect_v is the same as parent node, so it is not a vc
            # check it is not a dead end
            #   lower bound is the same as parent node, if it is less
            #         than the current best, add it to subproblems queue
            if len(available_vertices_delete_v) > 0 and self.still_is_cover(max_degree_v, available_vertices_delete_v, remaining_graph):
                if current_lb < current_best[0]:
                    sub_problems.push((tuple(cover_unselect_v), tuple(available_vertices_delete_v),
                                       sub_p[2], current_lb), remaining_graph.number_of_edges())

            # after cutoff_time, terminate and return the current best
            if time.time() - start_time > cutoff_time:
                break

        output_trace.close()
        output_result = open(result_file, 'w')
        output_result.write("%d\n" % (current_best[0]) )
        result = list(current_best[1])
        result = sorted(result)
        for i in range(current_best[0]-1):
            output_result.write("%d," % (result[i]))
        output_result.write("%d" % (result[-1]))
        output_result.close()

        return current_best


def run_bnb(input_file, cutoff_time):
    """this function provides an uniform interface for the other functions to call
       input: input_file (the input graph file), cutoff_time
       output: none
       side effect: save the trace file and solution file"""
    bnb_solver = bnb()

    start = input_file.rfind("/")
    end = input_file.find(".graph")
    filename = input_file[start+1:end]

    output_sol = "./output/" + filename + "_BnB_" + str(cutoff_time) + ".sol"
    output_trace = "./output/" + filename + "_BnB_" + str(cutoff_time) + ".trace"

    try:
        os.makedirs("./output")
    except OSError:
        if not os.path.isdir("./output"):
            raise

    G = read_graph(input_file)
    bnb_solver.bnb_edge_delection(G, cutoff_time, output_trace, output_sol)

if __name__ == '__main__':
    #run_bnb = bnb()
    #cProfile.run("run_bnb.pre_test()")
    run_bnb("./DATA/karate.graph", 30)
