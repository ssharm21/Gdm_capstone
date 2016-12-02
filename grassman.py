#Implementation of https://arxiv.org/abs/1303.2221
#Clustering on Multi-Layer Graphs via Subspace Analysis on Grassmann Manifolds
import numpy as np
from scipy.cluster.vq import kmeans2
import networkx as nx
import scipy.sparse.linalg as la
from scipy.sparse import csr_matrix

def getEigenDecomposition(lap, k):
	"""
	lap: numpy square matrix nXn 
	k: reduced dimesnion
	returns nXk matrix after eigen decomposition
	"""
	print lap.shape, type(lap)
	eig_val, eig_vec  = la.eigs(lap)
	top_indices = np.argsort(eig_val)[-k:]
	top_vecs = [eig_vec[:,i].transpose() for i in top_indices]
	print type(top_vecs)
	print top_vecs
	print type(np.vstack(top_vecs).T)
	return csr_matrix(np.vstack(top_vecs).T)

def getModifiedLap(lap_list, subspace_list, alpha):
	"""
	Gives modified laplacian according to eq (8)
	"""
	n = lap_list[0].shape[0]
	uu_dash = [csr_matrix(u.dot(u.T)) for u in subspace_list]
	lap_sum = np.zeros((n,n))
	uu_sum = np.zeros((n,n))

	for L in lap_list:
		lap_sum = np.add(lap_sum,L)
	for u in uu_sum:
		uu_sum = np.add(uu_sum,u)

	return np.subtract(lap_sum, aplpha * uu_dash) 

def findClustersGrassman(graph_list, k):
	"""
	graph_list : List of nx graphs Gi representing differnet layers
	"""
	alpha = 0.5
	num_layers = len(graph_list)

	#list of normalized Laplacian matrix Li for all Gi
	laplacian_list = [nx.normalized_laplacian_matrix(g)
	 for g in graph_list]

	#list of subspace representation Ui for all Gi
	subspace_list = [getEigenDecomposition(l, k) for l in laplacian_list]

	Lmod = getModifiedLap(laplacian_list,subspace_list, alpha)

	U = getEigenDecomposition(Lmod, k)

	#find clusters in U transpose
	centroids, labels = kmeans2(U.T,k,iter=20)

	return labels