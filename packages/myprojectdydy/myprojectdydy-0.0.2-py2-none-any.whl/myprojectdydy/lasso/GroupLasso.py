#ISTA(Iterative Shrinkage Thresholding Algorithm)
#L1 minimization  ||Ax-b||_2^2 + lambda * ||x||_G

import numpy as np      #import numpy
import matplotlib.pyplot as plt
from numpy import linalg as LA

def shrinkage(x,a):     #x: vector ,  a: scalar
    new_z = np.zeros(len(x))
    norm_x = LA.norm(x)

    if norm_x!=0:
        for k in range(len(x)):
            new_z[k] = max(norm_x - a,0) * x[k]/norm_x

    return new_z


def groupLasso(A,z,b,lamb1,lamb2,beta1,beta2, gamma1,gamma2,group, tol,shrinkage):   #solve a system Ax = b with groupLasso regularizer
    d = 100000
    iter = 0
    energy = np.zeros(10000)
    B = beta1*np.eye(len(A[0])) + beta2*np.dot(np.transpose(A),A)
    B_inv = LA.inv(B)
    z_new = np.zeros(np.shape(A)[1])
    z_new[:] = z[:]

    x_new = np.zeros(np.shape(A)[1])
    x_new[:] = z[:]
   # while (d > tol):
    while(iter < 1000):
        x_new[:] = np.dot(B_inv, beta1*z_new - lamb1 + beta2*np.dot(np.transpose(A),b) + np.dot(np.transpose(A),lamb2))[:]
        head = 0
        for k in range(len(group)):
            tail = head + group[k]
            z_new[head:tail] = shrinkage(x_new[head:tail]+1/beta1*lamb1[head:tail], 1/beta1)
            head = tail

        lamb1[:] = lamb1[:] - gamma1*beta1*(z_new[:] - x_new[:])
        lamb2[:] = lamb2[:] - gamma2*beta2*(np.dot(A,x_new)-b[:])

#        d = np.dot(np.transpose(x - x_new), x - x_new)/LA.norm(x)

        z[:] = z_new[:]
        x[:] = x_new[:]

        norm_z = 0
        head = 0

        for k in range(len(group)):
            tail = head+group[k]
            norm_z = norm_z + LA.norm(z_new[head:tail])
            head = tail

        energy[iter] = norm_z - np.dot(np.transpose(lamb1),z_new-x_new) + beta1/2 * LA.norm(z_new - x_new)**2 - np.dot(np.transpose(lamb2),np.dot(A,x_new)-b) + beta2/2 * LA.norm(np.dot(A,x) - b)**2
        iter = iter+1

    return z_new,energy[50:iter]

#A = np.array([[1.0,6.0,-1.0,-4.0,3.1,-2.4,5.2],[6.0,1.0,3.0,0.0,-1.4,0.33,-0.78],[4.0,1.0,-11.0,1.0,-5.3,4.6,1.08]])

if __name__=="__main__":
    A = np.array([[-2.4,5.2,-1.0,-4.0,3.1,1.0,6.0],[0.33,-0.78,3.0,0.0,-1.4,6.0,1.0],[4.6,1.08,-11.0,1.0,-5.3,4.0,1.0]])


    b = np.ones(np.shape(A)[0])
    x = np.ones(np.shape(A)[1])

    group = np.array([3,2,2])

    lamb1 = np.zeros(np.shape(A)[1])
    lamb2 = np.zeros(np.shape(A)[0])

    #beta1 = 1
    #beta2 = 5
    beta1 = 0.3/np.mean(abs(b))
    beta2 = 3/np.mean(abs(b))

    gamma1 = 1
    gamma2 = 1

    tol = 10**(-9)
    x_new, energy = groupLasso(A,x,b,lamb1,lamb2,beta1,beta2, gamma1,gamma2, group, tol,shrinkage)

    print(x_new)
    plt.plot(energy)
    plt.show()
