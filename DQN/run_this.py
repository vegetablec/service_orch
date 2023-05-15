import csv

import numpy as np
from padding import padding_data
from Qnetwork import DQnetwork
from calStep import StepCal
from read_nodeSet import readNodeSet
import time
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']


# 超参数配置
nodeSet = "./nodeSet_1.txt"
ALPHA = 0.01  # learning rate
GAMMA = 0.9    # reward_decay
EPSILON = 0.9  # e_greedy
MAX_EPISODES = 8000  # 最大迭代轮数
EXPERIENCE_POOL = 250 # 经验池大小
BATCH_SIZE = 250 # batch_size
REPLACE_TIME=200 # replace_time
screenflag = True
changeflag = True
changerate = 0.1
y = []
x = []
log = []

def changeData(services, rate):
    for i in range(len(services)):
        for j in range(len(services[i])):
            if np.random.rand() < rate:
                services[i][j][0] *= np.random.uniform(low=0.8, high=2)
                services[i][j][1] *= np.random.uniform(low=0.5, high=1.2)
                services[i][j][2] *= np.random.uniform(low=0.5, high=1.2)
                services[i][j][3] *= np.random.uniform(low=0.8, high=2)
    print('已改变{}%的数据'.format(rate*100))
    return services


def screenservice(services):
    for i in range(len(services)):
        j = 0
        while j < len(services[i]):
            if services[i][j][4] == 2 or services[i][j][4] == 3:
                del services[i][j]
                j -= 1
            j += 1

    maxactions = 0
    actions = []
    for i in range(len(services)):
        if maxactions < len(services[i]):
            maxactions = len(services[i])

    for i in range(len(services)):
        tempser = services[i][0]
        while maxactions > len(services[i]):
            services[i].append(tempser)
        actions.append(len(services[i]))

    return services, maxactions, actions


def DQN_run(max_actions, n_actions, n_features, node_num):
    start = time.time()
    DQN_agent = DQnetwork(max_actions=max_actions, n_actions=n_actions, n_features=n_features,
                          epsilon=EPSILON, batch_size=BATCH_SIZE,
                          learning_rate=ALPHA, gamma=GAMMA, replace_time=REPLACE_TIME,
                          n_experience_pool=EXPERIENCE_POOL)
    StepCalculater = StepCal(node_num, n_actions)
    StepCalculater.getMaxandMin()
    if screenflag:
        StepCalculater.service_data, maxactions, actions = screenservice(StepCalculater.service_data)
        DQN_agent.max_actions = maxactions
        DQN_agent.n_actions = actions
        print('筛选后最大服务数为{0}, 服务节点流为{1}'.format(maxactions, actions))
        StepCalculater.service_data = padding_data(max_actions, StepCalculater.service_data)
    DQN_agent.net_init_LSTM()
    max_reward = 0
    for episode in range(MAX_EPISODES):
        if changeflag and episode==2500:
            StepCalculater.service_data = changeData(StepCalculater.service_data, changerate)
            #StepCalculater.getMaxandMin()

        # 初始化
        state = 0
        choosen_actions = []
        total_reward = 0
        while True:
            #print(state)
            # get_env(StepCalculater.service_data)
            action = DQN_agent.choose_action([state])
            choosen_actions.append(action)
            # print(state, action)
            state_, reward, done = StepCalculater.step(state, choosen_actions)
            total_reward += reward
            DQN_agent.experience_store(s=[state], a=action, r=reward, s_=[state_], done=done)
            if (state + 1) % 5 == 0:
                DQN_agent.learn()

            state = state_

            if done:
                # if DQN_agent.epsilon <= 0.001:
                #     log.append(total_reward)
                # if total_reward - log[len(log)-1] >= 0.5:
                #     print("services = {0}, reward = {1}, runtime = {2}, episode = {3} ".format
                #           (choosen_actions, total_reward, time.time() - start, episode))
                # print("services = {0}, reward = {1}, runtime = {2}, episode = {3} ".format
                #       (choosen_actions, reward, time.time() - start, episode))
                if episode == 0:
                    max_reward = total_reward
                else:
                    if total_reward > max_reward:
                        max_reward = total_reward
                        print("services = {0}, reward = {1}, runtime = {2}, episode = {3} ".format
                              (choosen_actions, total_reward, time.time() - start, episode))

                    else:
                        if episode % 100 == 0:
                            print("episode = {0}, reward = {1}, services = {2}, ep = {3}".format(episode, total_reward, choosen_actions, DQN_agent.epsilon))
                        if episode % 10 == 0:
                            y.append(total_reward)
                            x.append(episode)

                break

    print("game over, runtime ={} ".format(time.time() - start))


if __name__ == "__main__":

    nodes_num, each_services_nums, all_services_nums, max_services_num = readNodeSet(nodeSet)
    print("1.服务节点数：{}".format(nodes_num))
    print("2.每个节点处候选子集大小：{}".format(each_services_nums))
    print("3.总的候选原子个数：{}".format(all_services_nums))
    print("4.最大候选子集个数：{}".format(max_services_num))

    DQN_run(max_services_num, each_services_nums, 1, nodes_num)
    plt.figure(figsize=(32, 8))
    plt.xlabel(u'迭代轮数', fontsize=30, color='k')
    plt.ylabel(u'总收益', fontsize=30, color='k')
    plt.xticks(fontproperties='Times New Roman', size=30)
    plt.yticks(fontproperties='Times New Roman', size=30)
    plt.plot(x, y, label='经验池容量为200', c='r')
    plt.legend(prop={'size': 30}, loc='best')
    #plt.savefig('Fex250.png')
    plt.show()
    with open('A_ADQNR_10%.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        header = ['episode', 'reward']
        writer.writerow(header)
        for i in range(len(x)):
            writer.writerow([x[i], y[i]])


