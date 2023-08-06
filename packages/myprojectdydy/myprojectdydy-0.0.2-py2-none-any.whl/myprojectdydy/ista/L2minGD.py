import numpy as np
from numpy import linalg as LA


def GDL2(x,a,lamb):
    n = len(x)
    deltax = np.zeros(n)
    stepsize = 0.00009
    normx = LA.norm(x)
    for k in range(n):
        deltax[k] = 2*(x[k]-a[k]) + lamb*1/normx*x[k]
        x[k] = x[k] - stepsize*deltax[k]
        normx = LA.norm(x)

    return x

if __name__=="__main__":
    a = np.array([1,1,1,1])
    lamb = 5
    x = np.ones(len(a))

    for kk in range(10000):
        x = GDL2(x,a,lamb)
        print(x)


