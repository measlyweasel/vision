from PIL import Image
from numpy import *

def pca(X):
    """
    Principal Component Analysis
        input: X, matrix with training data stored as flattened arrays in rows
        return: projection matrix ( with important dimensions first), variance and mean
    """

    #get dimensions
    num_data,dim = X.shape

    #center data
    mean_X = X.mean(axis=0) #mean axis=0 computes mean along each column, axis=1 is along each row