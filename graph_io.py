import networkx as nx

def read_graph(filename):
        """read in a graph file from filename, and return a graph object (as in networkx)"""
        with open(filename, 'r') as my_graph:
            num_line = my_graph.readline()

            num_data = list(map(lambda x: int(x), num_line.split()))
            assert(len(num_data) == 3)

            n, m = num_data[0], num_data[1]

            G = nx.Graph()
            i = 1
            for line in my_graph:
                edge_end = list(map(lambda x: int(x), line.split()))
                i_edges = [(i, v) for v in edge_end]
                G.add_edges_from(i_edges)
                i += 1

        return G

if __name__ == '__main__':
    filename ="karate.graph"
    G = read_graph(filename)
    print nx.number_of_nodes(G), nx.number_of_edges(G)
    print G.edges(1)
