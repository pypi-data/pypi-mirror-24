#ISTA(Iterative Shrinkage Thresholding Algorithm)
#L1 minimization  ||Ax-b||_2^2 + lambda * ||x||_2^2

import numpy as np      #import numpy
import matplotlib.pyplot as plt
from numpy import linalg as LA

def ISTA_it(A,x,b,lamb,C, tol):   #solve a system Ax = b with L1-regularizer
    d = 100000
    iter = 0
    energy = np.zeros(10000)
    while (d > tol):
        x_new = 1/(C+lamb) * (C*x - np.dot(np.transpose(A), np.dot(A,x)-b ))

        #print(x_new)

        d = np.dot(np.transpose(x - x_new),x-x_new)
        x = x_new

        energy[iter] = LA.norm(np.dot(A, x_new) - b) ** 2 + lamb * LA.norm(x_new)**2
        iter = iter+1

    return x,energy[100:iter]

if __name__ == "__main__":
    A = np.array([[1,6,-1,-4],[6,1,3,0],[4,1,-11,1]])
    b = np.transpose(np.array([1,1,1]))
    x = np.transpose(np.array([1,1,1,1]))
    lamb = 0.1
    C = 2* LA.norm(np.dot(np.transpose(A),A),2)
    tol = 10**(-9)

    x_new,energy = ISTA_it(A,x,b,lamb,C,tol)
    plt.plot(energy)
    plt.show()
