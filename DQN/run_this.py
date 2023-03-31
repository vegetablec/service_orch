from Qnetwork import DQnetwork
from calStep import StepCal
from read_nodeSet import readNodeSet
import time

# 超参数配置
nodeSet = "./nodeSet.txt"
outfile = "save/qlearning_10_1_1.txt"
ALPHA = 0.2  # learning rate
GAMMA = 0.9    # reward_decay
EPSILON = 0.9  # e_greedy
MAX_EPISODES = 3000  # 最大迭代轮数
EXPERIENCE_POOL = 1000 # 经验池大小
BATCH_SIZE = 64 # batch_size
REPLACE_TIME=300 # replace_time

def DQN_run(max_actions, n_actions, n_features, node_num):
    start = time.time()
    DQN_agent = DQnetwork(max_actions=max_actions, n_actions=n_actions, n_features=n_features,
                          epsilon=EPSILON, batch_size=BATCH_SIZE,
                          learning_rate=ALPHA, gamma=GAMMA, replace_time=REPLACE_TIME,
                          n_experience_pool=EXPERIENCE_POOL)
    StepCalculater = StepCal(node_num)
    DQN_agent.net_init()
    max_reward = 0
    for episode in range(MAX_EPISODES):
        # 初始化
        state = 0
        choosen_actions = []
        while True:
            #print(state)
            action = DQN_agent.choose_action([state])
            choosen_actions.append(action)
            # print(state, action)
            state_, reward, done = StepCalculater.step(state, choosen_actions)
            DQN_agent.experience_store(s=[state], a=action, r=reward, s_=[state_], done=done)
            DQN_agent.learn()
            state = state_

            if done:
                if episode == 0:
                    max_reward = reward
                else:
                    if reward > max_reward:
                        max_reward = reward
                        print("services = {0}, reward = {1}, runtime = {2}, episode = {3} ".format
                              (choosen_actions, reward, time.time() - start, episode))

                    else:
                        if episode % 100 == 0:
                            print("episode = {0}, reward = {1}, services = {2}".format(episode, reward, choosen_actions))

                break

    print("game over, runtime ={} ".format(time.time() - start))


if __name__ == "__main__":

    nodes_num, each_services_nums, all_services_nums, max_services_num = readNodeSet(nodeSet)
    print("1.服务节点数：{}".format(nodes_num))
    print("2.每个节点处候选子集大小：{}".format(each_services_nums))
    print("3.总的候选原子个数：{}".format(all_services_nums))
    print("4.最大候选子集个数：{}".format(max_services_num))

    DQN_run(max_services_num, each_services_nums, 1, nodes_num)


