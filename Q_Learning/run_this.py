import csv

import numpy as np
from calStep import StepCal
from RL_brain import QLearningTable
from read_nodeSet import readNodeSet
import time
import matplotlib.pyplot as plt


# 超参数配置
nodeSet = "./nodeSet_1.txt"
ALPHA = 0.2  # learning rate
GAMMA = 0.9    # reward_decay
EPSILON = 0.9  # e_greedy
MAX_EPISODES = 8000  # 最大迭代轮数
y = []
x = []
changeflag = True
changerate = 0.05

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


def update(nodes_num, each_services_nums, max_services_num):
    start = time.time()
    RL = QLearningTable(n_states=nodes_num, each_services_nums=each_services_nums,
                        max_services_num=max_services_num,
                        learning_rate=ALPHA, reward_decay=GAMMA, e_greedy=EPSILON)
    StepCalculater = StepCal(nodes_num, each_services_nums)
    StepCalculater.getMaxandMin()
    max_reward = 0

    for episode in range(MAX_EPISODES):
        if changeflag and episode==2500:
            StepCalculater.service_data = changeData(StepCalculater.service_data, changerate)
            #StepCalculater.getMaxandMin()
        # 初始化状态
        state = 0
        # print("episode = {}".format(episode))
        total_reward = 0
        choosen_actions = []
        while True:
            # 选择行为
            action = RL.choose_action(state)
            choosen_actions.append(action)
            # 进行选择并计算奖励
            state_, reward, done = StepCalculater.step(state, choosen_actions)
            total_reward += reward
            # print("s = {0}, a = {1}, s_ = {2}, reward = {3}, done = {4}".format(
            #     state, action, state_, reward, done
            # ))

            # 更新Q表
            RL.learn(state, action, reward, state_)

            # 进入下一状态
            state = state_

            # 本轮迭代结束跳出
            if done:
                # print("services = {0}, reward = {1}, runtime = {2}, episode = {3} ".format
                #       (RL.choose_services, reward, time.time()-start, episode))
                if episode == 0:
                    max_reward = total_reward
                    print("services = {0}, reward = {1}, runtime = {2}, episode = {3} ".format
                          (RL.choose_services, total_reward, time.time() - start, episode))
                else:
                    if total_reward > max_reward:
                        max_reward = total_reward
                        print("services = {0}, reward = {1}, runtime = {2}, episode = {3} ".format
                              (RL.choose_services, total_reward, time.time() - start, episode))
                    else:
                        if episode % 100 == 0:
                            print("episode = {0}, reward = {1}, epsilon = {2}".format(episode, total_reward, RL.epsilon))
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

    update(nodes_num, each_services_nums,max_services_num)
    plt.plot(x, y, c='r')
    plt.show()
    with open('A_QLearning_5%.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        header = ['episode', 'reward']
        writer.writerow(header)
        for i in range(len(x)):
            writer.writerow([x[i], y[i]])