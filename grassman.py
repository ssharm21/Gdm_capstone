#Implementation of https://arxiv.org/abs/1303.2221
#Clustering on Multi-Layer Graphs via Subspace Analysis on Grassmann Manifolds
import numpy as np
from scipy.cluster.vq import kmeans2
import networkx as nx
import scipy.sparse.linalg as la
from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize

def getEigenDecomposition(lap, k):
	"""
	lap: numpy square matrix nXn 
	k: reduced dimesnion
	returns nXk sparse matrix after eigen decomposition
	"""
	eig_val, eig_vec  = la.eigs(lap)
	top_indices = np.argsort(eig_val)[-k:]
	top_vecs = [eig_vec[:,i].transpose() for i in top_indices]
	return csr_matrix(np.vstack(top_vecs).T)	

def getModifiedLap(lap_list, subspace_list, alpha):
	"""
	Returns modified laplacian according to eq (8) in the paper
	"""
	n = lap_list[0].shape[0]
	uu_dash = [u.dot(u.T) for u in subspace_list]
	
	lap_sum = np.zeros((n,n))
	uu_sum = np.zeros((n,n))
	for L in lap_list:
		lap_sum = np.add(lap_sum,L.todense())
	for u in uu_dash:
		uu_sum = np.add(uu_sum,u.todense())
	
	return np.subtract(lap_sum, alpha * uu_sum) 

def findClustersGrassman(graph_list, k, alpha):
	"""
	graph_list : List of nx graphs Gi representing differnet layers
	"""
	num_layers = len(graph_list)

	print 'Finding clusters using subspace analysis on Grassman Manifolds....'
	print 'alpha = ', alpha
	#list of normalized Laplacian matrix Li for all Gi
	laplacian_list = [nx.normalized_laplacian_matrix(g, nodelist = sorted(g.nodes()))
	 for g in graph_list]
	#list of subspace representation Ui for all Gi
	subspace_list = [getEigenDecomposition(l, k) for l in laplacian_list]
       
	Lmod = getModifiedLap(laplacian_list,subspace_list, alpha)

	U = getEigenDecomposition(Lmod, k).real.todense()
       
	U = normalize(U, axis=1, norm='l1')
     
	#find clusters in U
	centroids, labels = kmeans2(U,k,iter=20)

	return labels
