import numpy as np
import networkx as nx
import preprocessing as pre


def number_of_nodes_in_cluster(labels):
    colors = {}
    for v,c in enumerate(labels):
        if c in colors:
            colors[c] += 1
	else:
	    colors[c] = 0
    print colors

def find_avg_cluster_density(labels, graph_list):
    colors = {}
    for v,c in enumerate(labels):
        if c in colors:
            colors[c] += [v]
	else:
	    colors[c] = [v]
 
    density = np.zeros((len(graph_list),len(colors)))
    for k in colors:
        for i,g in enumerate(graph_list):
            node_list = sorted(g.nodes())
            list_new = []
            for i in colors[k]:
                list_new += node_list[i]
            print len(list_new)
            print len(list(set(list_new).intersection(set(g.nodes()))))
            exit()
            density[i,k] = nx.density(g.subgraph(colors[k]))
    print density

        
    
