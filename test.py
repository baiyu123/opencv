import numpy as np
from numpy.linalg import inv
A = np.matrix(((1,2),(3,4)))
B = inv(A)
print B