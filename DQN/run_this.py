import numpy as np
from padding import padding_data
from Qnetwork import DQnetwork
from calStep import StepCal
from read_nodeSet import readNodeSet
import time
import matplotlib.pyplot as plt


# 超参数配置
nodeSet = "./nodeSet_1.txt"
outfile = "save/qlearning_10_1_1.txt"
ALPHA = 0.01  # learning rate
GAMMA = 0.9    # reward_decay
EPSILON = 0.8  # e_greedy
MAX_EPISODES = 2500  # 最大迭代轮数
EXPERIENCE_POOL = 200 # 经验池大小
BATCH_SIZE = 64 # batch_size
REPLACE_TIME=200 # replace_time
y = []
x = []
log = []

def DQN_run(max_actions, n_actions, n_features, node_num):
    start = time.time()
    DQN_agent = DQnetwork(max_actions=max_actions, n_actions=n_actions, n_features=n_features,
                          epsilon=EPSILON, batch_size=BATCH_SIZE,
                          learning_rate=ALPHA, gamma=GAMMA, replace_time=REPLACE_TIME,
                          n_experience_pool=EXPERIENCE_POOL)
    StepCalculater = StepCal(node_num)
    StepCalculater.service_data = padding_data(max_actions, StepCalculater.service_data)
    DQN_agent.net_init_LSTM()
    max_reward = 0
    for episode in range(MAX_EPISODES):
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
    plt.plot(x, y, c='r')
    plt.show()


