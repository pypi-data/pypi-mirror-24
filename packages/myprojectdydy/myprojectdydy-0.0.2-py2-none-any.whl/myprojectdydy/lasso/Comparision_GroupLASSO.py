import GroupLasso2
import GroupLasso_ISTA
import numpy as np      #import numpy
import matplotlib.pyplot as plt
from numpy import linalg as LA


#A = np.array([[-2.4,5.2,-1.0,-4.0,3.1,1.0,6.0],[0.33,-0.78,3.0,0.0,-1.4,6.0,1.0],[4.6,1.08,-11.0,1.0,-5.3,4.0,1.0]])

#rows = 4
#cols = 3
A = 100*np.random.rand(3,7)
print(np.shape(A))


b = np.ones(np.shape(A)[0])
x = np.ones(np.shape(A)[1])

lamb1 = np.zeros(np.shape(A)[1])
lamb2 = np.zeros(np.shape(A)[0])
group = np.array([3, 2, 2])

#group = np.ones(40)
#group = group.astype(np.int)
#group[:] = 5
#print(group)
#group = np.array([10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10])
tol = 10**(-9)


#set parameters
beta1 = 0.3/np.mean(abs(b))
beta2 = 3/np.mean(abs(b))
gamma1 = 1.618
gamma2 = 1.618

x_new, energy = GroupLasso2.groupLasso(A,x,b,lamb1,lamb2,beta1,beta2, gamma1,gamma2, group, tol, GroupLasso2.shrinkage)

lamb = 2/beta2
C = LA.norm(np.dot(np.transpose(A),A),2)

x = np.ones(np.shape(A)[1])
x_new2,energy2 = GroupLasso_ISTA.ISTA_it(A,x,b,beta2,C,group,tol,GroupLasso_ISTA.shrinkage)

print(LA.norm(x_new-x_new2))
plt.figure(figsize=(10,6), dpi=80)
plt.plot(energy[:10000],color="blue",label="Proximal Gradient")
plt.plot(energy2[:10000],color="red", label="ISTA")

print('------------Condition number of the matrix---------')
print(LA.cond(np.dot(np.transpose(A),A),2))
print('------------Sol of Proximal Grad ------------')
print(x_new)
print('------------Sol of ISTA ------------')
print(x_new2)
#print('------------Exact Sol ------------')
#print(np.dot(LA.inv(A),b))

#plt.ylim(-.5, .5)
print('Error of a result using Proximal Gradient : ',energy[:10000])
print('Error of a result using ISTA : ',energy2[:10000])
plt.legend(loc='upper left', frameon=False)
plt.show()
