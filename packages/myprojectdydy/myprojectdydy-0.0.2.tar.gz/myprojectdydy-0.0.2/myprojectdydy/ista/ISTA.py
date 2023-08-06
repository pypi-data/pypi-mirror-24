#ISTA(Iterative Shrinkage Thresholding Algorithm)
#L1 minimization  ||Ax-b||_2^2 + lambda * ||x||_1

import numpy as np      #import numpy
import matplotlib.pyplot as plt
from numpy import linalg as LA


def threshold(x,lamb,C):
    if x < -lamb/2/C:
        gamma_x = x + lamb/2/C
    elif x > lamb/2/C:
        gamma_x = x - lamb/2/C
    else:
        gamma_x = 0
    return gamma_x


def ISTA_it(A,x,b,lamb,C, tol,threshold):   #solve a system Ax = b with L1-regularizer
    d = 100000
    iter = 0
    energy = np.zeros(50000)
    x_new = np.zeros(np.shape(A)[1])

   # while (d > tol):
    while(iter<20000):
        y = x + 1/C* np.dot(np.transpose(A),b-np.dot(A,x))

        for k in range(len(y)):
            x_new[k] = threshold(y[k],lamb,C)

       # print(x_new)

        d = np.dot(np.transpose(x - x_new),x-x_new)
        x[:] = x_new[:]

        energy[iter] = LA.norm(np.dot(A, x_new) - b) ** 2 + lamb * LA.norm(x_new, 1)
        iter = iter+1

    return x,energy[100:iter]

if __name__ == "__main__":
    #A = np.array([[1.0,6.0,-1.0,-4.0,3.1,-2.4,5.2],[6.0,1.0,3.0,0.0,-1.4,0.33,-0.78],[4.0,1.0,-11.0,1.0,-5.3,4.6,1.08]])
    A = np.random.rand(7, 7)
    b = np.ones(np.shape(A)[0])
    x = np.ones(np.shape(A)[1])

    lamb = 0
    C = 2* LA.norm(np.dot(np.transpose(A),A),2)
    tol = 10**(-9)

    x_new,energy = ISTA_it(A,x,b,lamb,C,tol,threshold)

    print(energy)
    print('------------Sol of ISTA ------------')
    print(x_new)
    print('------------Exact Sol ------------')
    print(np.dot(LA.inv(A), b))

    plt.plot(energy)

    plt.show()
