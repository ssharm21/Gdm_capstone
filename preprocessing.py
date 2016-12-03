#python preprocessing.py higgs-reply_network.edgelist higgs-mention_network.edgelist higgs-social_network.edgelist
#python preprocessing.py data/higgs-reply_network.edgelist data/higgs-mention_network.edgelist data/higgs-retweet_network.edgelist
#python preprocessing.py data/edge_list_airline-europe_layer1.txt data/edge_list_airline-europe_layer2.txt data/edge_list_airline-europe_layer4.txt
import sys
import  networkx as nx
import numpy as np
import csv
import grassman
import evaluate
import random

def generate_graph2(filename1, list_of_nodes):
    G=nx.Graph()
    with open(filename1,'rb') as inf:
        inf_read =csv.reader(inf, delimiter = ' ')
        list1 = set()
        for row in inf_read:
            if row[0] in list_of_nodes and row[1] in list_of_nodes:
                G.add_edge(row[0],row[1])
    return G

def generate_graph(filename):
    with open(filename, 'rb') as inf:
        G = nx.read_edgelist(inf, delimiter=" ", nodetype=int, data=(('weight',float),))
    return G

def filter_nodes(G1, G2, G3):
    G2 = G2.subgraph(G1.nodes())
    G3 = G3.subgraph(G1.nodes())
    return G2, G3
 

def main():
    reply_file = sys.argv[1]
    mention_file = sys.argv[2]
    retweet_file = sys.argv[3]
    G_reply = generate_graph(reply_file)
    print "Graph reply created"
    G_mention = generate_graph(mention_file)
    print "Graph mention created"
    G_retweet = generate_graph(retweet_file)
    print "Graph retweet created"
    '''
    print ("nodes in reply: ", nx.number_of_nodes(G_reply))
    print ("nodes in mention: ", nx.number_of_nodes(G_mention))
    print ("nodes in retweet: ", nx.number_of_nodes(G_retweet))
    print "Filtering..."
    '''
    G_mention, G_retweet = filter_nodes(G_reply,G_mention,G_retweet)
    '''
    print ("nodes in reply: ", nx.number_of_nodes(G_reply))
    print ("nodes in mention: ", nx.number_of_nodes(G_mention))
    print ("nodes in retweet: ", nx.number_of_nodes(G_retweet))
    '''
    G_reply, G_mention = filter_nodes(G_retweet,G_reply,G_mention)
    '''
    print ("nodes in reply: ", nx.number_of_nodes(G_reply))
    print ("nodes in mention: ", nx.number_of_nodes(G_mention))
    print ("nodes in retweet: ", nx.number_of_nodes(G_retweet))
    '''
    print ("selecting 3000 nodes")

    sel_idx = random.sample(range(21346),3000)
    G_reply = G_reply.subgraph([n for i,n in enumerate(G_reply.nodes()) if i in sel_idx])
    G_mention, G_retweet = filter_nodes(G_reply,G_mention,G_retweet)
    print ("nodes in reply: ", nx.number_of_nodes(G_reply))
    print ("nodes in mention: ", nx.number_of_nodes(G_mention))
    print ("nodes in retweet: ", nx.number_of_nodes(G_retweet))
    
    graph_list = [G_reply,G_mention,G_retweet]
    labels = grassman.findClustersGrassman(graph_list,5)
    evaluate.find_avg_cluster_density(labels,graph_list)

if __name__ == '__main__':
    main()
