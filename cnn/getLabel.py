import csv
import numpy as np

maxqos = [0, 100, 100, 0]
minqos = [9999, 0, 0, 9999]

def readdata(url):
    with open(url, 'r', newline='') as file:
        reader = csv.DictReader(file)
        data = []
        for row in reader:
            onedata = []
            onedata.append(float(row['RT']))
            onedata.append(float(row['Avai']))
            onedata.append(float(row['Thr']))
            onedata.append(float(row['Late']))
            onedata.append(int(row['Place']))
            data.append(onedata)
    return data

def getLate(place):
    delay = 0
    if place == 0:
        delay = np.random.randint(1, 10)
    elif place == 1:
        delay = np.random.randint(500, 1000)
    elif place == 2:
        delay = np.random.randint(500, 1000)
    elif place == 3:
        delay = np.random.randint(10, 700)
    return delay

def getscore(r):
    f1 = ((9999 - r[0]) / (9999)) + \
         ((r[1] - 0) / (100)) + \
         ((r[2] - 0) / (100)) + \
         ((9999 - getLate(r[4])) / (9999))
    f = 1.0 / 4 * f1
    return f

data = readdata("traindata.csv")
for onedata in data:
    score = round(getscore(onedata), 5)
    onedata.append(score)
print(data)
with open('traindata_label.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    header = ['RT', 'Avai', 'Thr', 'Late', 'Place', 'Label']
    writer.writerow(header)
    writer.writerows(data)