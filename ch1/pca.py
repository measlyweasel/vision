from PIL import Image
from numpy import *

def pca(X):
    """
    Principal Component Analysis
        input: X, matrix with training data stored as flattened arrays in rows
        return: projection matrix ( with important dimensions first), variance and mean
    """

    #get number of data types (i.e. columns,original components), and dimensions (i.e. # of samples)
    num_data_types,dimensions = X.shape

    #center data
    mean_X = X.mean(axis=0) #mean axis=0 computes mean along each column, axis=1 is along each row
    X = X - mean_X

    if dimensions>num_data_types:
        #use the PCA compacting trick
        M = dot(X,X.T) #covariance matrix
        e,EV = linalg.eigh(M) #eigenvalues and eigenvectors
        tmp = dot(X.T, EV).T # this is the compacting trick
        V=tmp[::-1] #reverse since last eigenvectors are the ones we want
        S=sqrt(e)[::-1] # reverse since eigenvalues are in increasing order
        for i in range(V.shape[1]):
            V[:,i] /= S
    else:
        #PCA - use Singular Value Decomposition (SVD)
        U,S,V = linalg.svd(X)
        V=V[:num_data_types]

    #return the projection matrix, the variance and the mean
    return V,S,mean_X