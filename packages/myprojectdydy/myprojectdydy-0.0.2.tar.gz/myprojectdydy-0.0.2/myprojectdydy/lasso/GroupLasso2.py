#ISTA(Iterative Shrinkage Thresholding Algorithm)
#L1 minimization  ||Ax-b||_2^2 + lambda * ||x||_G

import numpy as np      #import numpy
import matplotlib.pyplot as plt
from numpy import linalg as LA

def shrinkage(x,a):     #x: vector ,  a: scalar
    new_z = np.zeros(len(x))
    norm_x = LA.norm(x)

    if norm_x - a/2 < 0:
        pass
    else:
        new_z = (1-a/2/norm_x)*x

    return new_z


def groupLasso(A,z,b,lamb1,lamb2,beta1,beta2, gamma1,gamma2,group, tol, shrinkage):   #solve a system Ax = b with groupLasso regularizer
    d = 100000
    iter = 0
    energy = np.zeros(20000)
    B = beta1*np.eye(len(A[0])) + beta2*np.dot(np.transpose(A),A)
    B_inv = LA.inv(B)
    x_new = np.ones(np.shape(A)[1])

    while(iter < 20000):

        norm_z = 0
        head = 0

        for k in range(len(group)):
            tail = head + group[k]
            norm_z = norm_z + LA.norm(x_new[head:tail])
            head = tail

        energy[iter] = beta2/2 * LA.norm(np.dot(A, x_new) - b) ** 2 + norm_z


        x_new = np.dot(B_inv, beta1*z - lamb1 + beta2*np.dot(np.transpose(A),b) + np.dot(np.transpose(A),lamb2))
        head = 0
        for k in range(len(group)):
            tail = head + group[k]
            z[head:tail] = shrinkage(x_new[head:tail]+1/beta1*lamb1[head:tail], 1/beta1)[:]
            head = tail

        lamb1 -= gamma1*beta1*(z[:] - x_new[:])
        lamb2 -= gamma2*beta2*(np.dot(A,x_new)-b[:])

        norm_z = 0
        head = 0

        for k in range(len(group)):
            tail = head+group[k]
            norm_z += LA.norm(z[head:tail])
            head = tail

        iter += 1


    return x_new,energy[5000:]

#A = np.array([[1.0,6.0,-1.0,-4.0,3.1,-2.4,5.2],[6.0,1.0,3.0,0.0,-1.4,0.33,-0.78],[4.0,1.0,-11.0,1.0,-5.3,4.6,1.08]])

if __name__ == "__main__":

   # A = np.array([[-2.4,5.2,-1.0,-4.0,3.1,1.0,6.0],[0.33,-0.78,3.0,0.0,-1.4,6.0,1.0],[4.6,1.08,-11.0,1.0,-5.3,4.0,1.0]])
    A = 100*np.random.rand(3, 7)
   # group = np.ones(100)
   # group = group.astype(np.int)
   # group[:] = 2


    #initialize all variables
    b = np.ones(np.shape(A)[0])
    x = np.ones(np.shape(A)[1])
    lamb1 = np.zeros(np.shape(A)[1])
    lamb2 = np.zeros(np.shape(A)[0])

    #set parameters
    beta1 = 0.3/np.mean(abs(b))
    beta2 = 3/np.mean(abs(b))
    gamma1 = 1
    gamma2 = 1
    tol = 10**(-9)

    group = np.array([3,2,2])
    x_new, energy = groupLasso(A,x,b,lamb1,lamb2,beta1,beta2, gamma1,gamma2, group, tol, shrinkage)
    norm_z = 0
    head = 0

    for k in range(len(group)):
        tail = head + group[k]
        norm_z = norm_z + LA.norm(x_new[head:tail])
        head = tail

    print(norm_z)



    print(energy[:100])


    print(x_new)
    plt.plot(energy)
    plt.show()

