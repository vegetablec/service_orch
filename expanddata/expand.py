import random

from dataproc import getdata
import numpy as np
import csv

data = list(getdata())
def getMaxRT():
    max = 0
    for i in range(len(data)):
        if max < data[i][0]:
            max = data[i][0]
    return max

def getMinRT():
    min = 99999
    for i in range(len(data)):
        if min > data[i][0]:
            min = data[i][0]
    return min

def getMaxAvai():
    max = 0
    for i in range(len(data)):
        if max < data[i][1]:
            max = data[i][1]
    return max

def getMinAvai():
    min = 99999
    for i in range(len(data)):
        if min > data[i][1]:
            min = data[i][1]
    return min

def getMaxThr():
    max = 0
    for i in range(len(data)):
        if max < data[i][2]:
            max = data[i][2]
    return max

def getMinThr():
    min = 99999
    for i in range(len(data)):
        if min > data[i][2]:
            min = data[i][2]
    return min

def createdata(maxRT, minRT, maxAvai, minAvai, maxThr, minThr):
    RT = np.random.uniform(low=(np.random.uniform(low=minRT * 0.7, high=minRT * 1.1)), high=(np.random.uniform(low=maxRT * 0.7, high=maxRT * 1.1)))
    Avai = np.random.uniform(low=(np.random.uniform(low=minAvai * 0.7, high=minAvai * 1.1)), high=(np.random.uniform(low=maxAvai * 0.7, high=maxAvai * 1.1)))
    Thr = np.random.uniform(low=(np.random.uniform(low=minThr * 0.7, high=minThr * 1.1)), high=(np.random.uniform(low=maxThr * 0.7, high=maxThr * 1.1)))
    return [round(RT, 1), round(Avai, 1), round(Thr, 1)]

def getpalanddel():
    place = np.random.randint(0,4)
    delay = 0
    if place==0:
        delay = np.random.randint(1,10)
    elif place==1:
        delay = np.random.randint(500, 1000)
    elif place==2:
        delay = np.random.randint(500, 1000)
    elif place==3:
        delay = np.random.randint(10, 700)

    return delay, place

if __name__=='__main__':
    maxRT = getMaxRT()
    minRT = getMinRT()
    maxAvai = getMaxAvai()
    minAvai = getMinAvai()
    maxThr = getMaxThr()
    minThr = getMinThr()
    print(maxRT, minRT, maxAvai, minAvai, maxThr, minThr)
    alldata = []
    for i in range(2507):
        alldata.append(list(data[i]))
    for i in range(7493):
        randata = createdata(maxRT, minRT, maxAvai, minAvai, maxThr, minThr)
        alldata.append(randata)
    for data in alldata:
        delay, place = getpalanddel()
        data.append(delay)
        data.append(place)
    random.shuffle(alldata)
    print(alldata)
    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        header = ['RT', 'Avai', 'Thr', 'Late', 'Place']
        writer.writerow(header)
        writer.writerows(alldata)
        # for p in alldata:
        #     writer.writerow(p)