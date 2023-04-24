import math
import numpy as np
from numpy.linalg import norm

# def cossim(m):
#     lst = []
#     for i in range(len(m)):
#         for j in range(i,len(m)):
#             a = np.array(m[i])
#             b = np.array(m[j])
#             lst.append(np.dot(a,b)/(norm(a)*norm(b)))
    
#     m_t = np.array(m).transpose()
#     for i in range(len(m)):
#         for j in range(i,len(m)):
#             a = np.array(m[i])
#             b = np.array(m[j])
#             lst.append(np.dot(a,b)/(norm(a)*norm(b)))
    
#     return sum(lst) / len(lst)


def score(m):
    return sum([sum(row) for row in m])/(len(m))**2


ma = [[0.9, 0.9], [1,1]]
print(score(ma))
mb = [[0.4, 0.4], [0.5,0.5]]
print(score(mb))





