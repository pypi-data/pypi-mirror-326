import numpy as np
from numpy.typing import NDArray

from scipy.sparse import csc_matrix, hstack

def _construct_adj_matrix(matrix: NDArray
                          ) -> csc_matrix:
    """
    Construct a sparse adjacency matrix from a clustering matrix.

    This function constructs a sparse adjacency matrix from a clustering matrix, where each column represents
    a clustering solution, and each row represents an element being clustered. It converts each clustering
    solution into a binary matrix and concatenates them horizontally to form the adjacency matrix.

    Parameters
    ----------
    matrix : ndarray
        A 2D array where each column represents a clustering solution, and each row represents an element being clustered.

    Returns
    -------
    csc_matrix
        A sparse adjacency matrix in Compressed Sparse Column (CSC) format.
    """

    binary_matrices = []
    for solution in matrix.T:
        clusters = np.unique(solution)
        binary_matrix = (solution[:, np.newaxis] == clusters).astype(bool)
        binary_matrices.append(csc_matrix(binary_matrix, dtype=bool))

    return hstack(binary_matrices, format='csc', dtype=bool)