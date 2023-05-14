import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
import csv


def readdata(url):
    x=[]
    y=[]
    with open(url, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if (int(row['episode']))%500 == 0 or int(row['episode'])==10or int(row['episode'])==7990:
                x.append(round(float(row['episode']), 1))
                y.append(round(float(row['reward']), 1))
    return x, y

dqn_x, dqn_y = readdata('DQN.csv')
adqnr_x, adqnr_y = readdata('ADQNR.csv')
ql_x, ql_y = readdata('QLearning.csv')

plt.figure(figsize=(32, 8))
plt.xlabel(u'迭代轮数', fontsize=30, color='k')
plt.ylabel(u'总收益', fontsize=30, color='k')
plt.xticks(fontproperties='Times New Roman', size=30)
plt.yticks(fontproperties='Times New Roman', size=30)
line1 = plt.plot(dqn_x, dqn_y, label='ADQNR', c='r')
line2 = plt.plot(adqnr_x, adqnr_y, label='进行服务筛选的ADQNR', c='k')
line3 = plt.plot(ql_x, ql_y, label='Q_Learning', c='b')
plt.legend(prop={'size': 30}, loc='best')
plt.savefig('data.png')
plt.show()