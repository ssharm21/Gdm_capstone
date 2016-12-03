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
    order = sorted(graph_list[0].nodes())
    colors = {}
    for i,c in enumerate(labels):
        if c in colors:
            colors[c] += [order[i]]
	else:
	    colors[c] = [order[i]]
    density = np.zeros((len(graph_list),len(colors)))
    conductance = np.zeros((len(graph_list),len(colors)))
    for i,g in enumerate(graph_list):
        A = nx.adjacency_matrix(g).todense()
        for k in colors:
            #print len(colors[k])
            #print len(list(set(colors[k]).intersection(set(g.nodes()))))
            g_sub = g.subgraph(colors[k])
            density[i,k] = nx.density(g_sub)
            
            ms = nx.number_of_edges(g_sub)
            cluster_vertex = g_sub.nodes()
            cs = 0
            for cv in cluster_vertex:
                cs += len(set(g.neighbors(cv))-set(cluster_vertex))
            conductance[i,k] = float(cs)/((2*ms)+cs)
    print np.mean(density,axis=0)
    print np.mean(conductance,axis=0)

        
    
