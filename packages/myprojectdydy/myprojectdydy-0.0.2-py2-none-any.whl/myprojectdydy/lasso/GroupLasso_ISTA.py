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

def shrinkage(x,a):     #x: vector ,  a: scalar
    new_z = np.zeros(len(x))
    norm_x = LA.norm(x)

    if norm_x - a/2 < 0:
        pass
    else:
        new_z = (1-a/2/norm_x)*x

    return new_z

def ISTA_1(A,x,b,lamb,C, tol,threshold):   #solve a system Ax = b with L1-regularizer
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


def ISTA_it(A,x,b,beta2,C, group, tol,shrinkage):   #solve a system Ax = b with L1-regularizer
#def ISTA_it(A, x, b, lamb, C, group, tol, shrinkage):
    d = 100000
    iter = 0
    energy = np.zeros(2000000)
    t = 1
 #   while (d > tol):
    while(iter<1000000):
        norm_z = 0
        head = 0
        #Calculate Group norm
        for k in range(len(group)):
            tail = head + group[k]
            norm_z = norm_z + LA.norm(x[head:tail])
            head = tail
        #Calculate cost function for each step
        energy[iter] = beta2/2 * LA.norm(np.dot(A, x) - b) ** 2 + norm_z
        y = x + 1/C * np.dot(np.transpose(A), b - np.dot(A, x))

        head = 0
        tmp = np.zeros(len(x))
        x_new = np.zeros(len(x))
        for k in range(len(group)):
            tail = head + group[k]
            #tmp[head:tail] = shrinkage(y[head:tail], lamb / C)
            tmp[head:tail] = shrinkage(y[head:tail], 2 / beta2/C)
            head = tail

        x_new[:] = tmp[:]
        new_t = 0.5*(1+np.sqrt(4*t*t+1))
        xx_new = (1+(t-1)/new_t)*x_new - (t-1)/new_t*x


        x[:] = xx_new[:]
        t = new_t

        iter = iter+1

    return x,energy[100:]

if __name__=="__main__":

   # A = np.array([[-2.4,5.2,-1.0,-4.0,3.1,1.0,6.0],[0.33,-0.78,3.0,0.0,-1.4,6.0,1.0],[4.6,1.08,-11.0,1.0,-5.3,4.0,1.0]])
    #A = 100 * np.random.rand(3,7)
    A = [[1, -2, 3, 4, 0, 6, 7],
   [8, 0, -2, -11, 2, 1, -4],
   [1, 1, 7, 8, 19, 20, -21],
   [2, 3, -4, 5, 26, 7, 28],
   [2, -30, 1, 2, 3, 4, 35],
   [3, -7, 8, 9, 0, 4, 2],
   [4, 4, 5, -6, 7, 4, 9]]

    AA = LA.inv(A)
    print(np.dot(A,AA))
    b = np.ones(np.shape(A)[0])
    x = np.ones(np.shape(A)[1])
   # group = np.ones(100)
   # group = group.astype(np.int)
   # group[:] = 2

 #   beta2 = 3 / np.mean(abs(b))
    beta2 = 0.0

    C = 2.0* LA.norm(np.dot(np.transpose(A),A),2)
    tol = 10**(-9)
    group = np.array([3,2,2])

    x_new0, energy0 = ISTA_1(A,x,b,beta2,C,tol,threshold)

    b = np.ones(np.shape(A)[0])
    x = np.ones(np.shape(A)[1])

    x_new,energy = ISTA_it(A,x,b,beta2,C,group,tol,shrinkage)

    print('------------Sol of ISTA1 ------------')
    print(x_new0)
    print('------------Sol of ISTA_group ------------')
    print(x_new)
    print('------------Exact sol ------------')
    print(np.dot(LA.inv(A), b))
