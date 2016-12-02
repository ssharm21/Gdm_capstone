#python preprocessing.py higgs-reply_network.edgelist higgs-mention_network.edgelist higgs-social_network.edgelist
#python preprocessing.py higgs-reply_network.edgelist higgs-mention_network.edgelist higgs-retweet_network.edgelist
import sys
import  networkx as nx
import numpy as np
import csv
import grassman

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
        G = nx.read_edgelist(inf, delimiter=" ", nodetype=str, data=(('weight',float),))
    return G

def filter_nodes(G_reply, G_mention, G_retweet):
    G_mention = G_mention.subgraph(G_reply.nodes())
    G_retweet = G_retweet.subgraph(G_reply.nodes())
    return G_mention, G_retweet
 

def main():
    reply_file = sys.argv[1]
    mention_file = sys.argv[2]
    retweet_file = sys.argv[3]
    G_reply = generate_graph(reply_file)
    print "Graph reply created"
    G_mention = generate_graph(mention_file)
    print "Graph mention created"
    #G_social = generate_graph2(social_file, list(G_reply.nodes()))
    G_retweet = generate_graph(retweet_file)
    print "Graph retweet created"
    print ("nodes in reply: ", nx.number_of_nodes(G_reply))
    print ("nodes in mention: ", nx.number_of_nodes(G_mention))
    print ("nodes in retweet: ", nx.number_of_nodes(G_retweet))
    print "Filtering..."
    G_mention, G_retweet = filter_nodes(G_reply,G_mention,G_retweet)
    print ("nodes in reply: ", nx.number_of_nodes(G_reply))
    print ("nodes in mention: ", nx.number_of_nodes(G_mention))
    print ("nodes in retweet: ", nx.number_of_nodes(G_retweet))
    print grassman.findClustersGrassman([G_reply,G_mention,G_retweet],6)

if __name__ == '__main__':
    main()
