import numpy as np
import dataproc

a = [[1,2,3,20,5,6,7,8,9,10,11,12,13]]
a = np.array(a)
print(np.argmax(a[:, 0:10]))
for i in range(0,10):
    print(i)
data = dataproc.getdata()
for i in range(10):
    print(len(data[i]))
