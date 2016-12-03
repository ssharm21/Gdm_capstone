import numpy as np
import networkx as nx
import preprocessing as pre

def printAverageNodesInCluster(colors):
    print {c:len(colors[c]) for c in colors}
    
def evaluateClusters(labels, graph_list):
    order = sorted(graph_list[0].nodes())
    colors = {}
    num_layers = len(graph_list)
    for i,c in enumerate(labels):
        if c in colors:
            colors[c] += [order[i]]
	else:
	    colors[c] = [order[i]]



    density = np.zeros((num_layers,len(colors)))
    conductance = np.zeros((num_layers,len(colors)))
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
                if ms == 0 and cs == 0:
                    conductance[i,k] = 1
                else:
                    conductance[i,k] = float(cs)/((2*ms)+cs)
    print "Density found for each cluster across all layers:"
    print np.mean(density,axis=0)
    print "Conductance found for each cluster across all layers:"
    print np.mean(conductance,axis=0)
    mean_density = np.sum(np.mean(density,axis=0))/num_layers
    mean_conductance = np.sum(np.mean(conductance,axis=0))/num_layers
    return mean_density, mean_conductance

        
    
