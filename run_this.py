from RL_brain import QLearningTable
import time

# 超参数配置
nodeSet = "./nodeSet.txt"
outfile = "save/qlearning_10_1_1.txt"
ALPHA = 0.2  # learning rate
GAMMA = 0.9    # reward_decay
EPSILON = 0.60  # e_greedy
MAX_EPISODES = 3000  # 最大迭代轮数
ERROR_COUNT = 50   # 连续100次，reward变化在误差允许范围内，则提前终止实验
ERROR_RANGE = 0.0001   # 误差范围
judge_list = []


def update():
    start = time.time()
    RL = QLearningTable(n_states=nodes_num, each_services_nums=each_services_nums,
                        max_services_num=max_services_num,
                        learning_rate=ALPHA, reward_decay=GAMMA, e_greedy=EPSILON)
    max_reward = 0

    for episode in range(MAX_EPISODES):
        # 初始化状态
        state = 0
        # print("episode = {}".format(episode))

        while True:
            # 选择行为
            action = RL.choose_action(state)

            # 进行选择并计算奖励
            state_, reward, done = RL.step(state, action)

            print("s = {0}, a = {1}, s_ = {2}, reward = {3}".format(
                state, action, state_, reward
            ))

            # 更新Q表
            RL.learn(state, action, reward, state_)

            # 进入下一状态
            state = state_

            # 本轮迭代结束跳出
            if done:
                # print("services = {0}, reward = {1}, runtime = {2}, episode = {3} ".format
                #       (RL.choose_services, reward, time.time()-start, episode))
                if episode == 0:
                    max_reward = reward
                else:
                    if reward > max_reward:
                        max_reward = reward
                        print("services = {0}, reward = {1}, runtime = {2}, episode = {3} ".format
                              (RL.choose_services, reward, time.time() - start, episode))
                    else:
                        if episode % 100 == 0:
                            print("episode = {}".format(episode))
                break

        # 终止条件
        if episode >= ERROR_COUNT:
            del judge_list[0]
        judge_list.append(reward)

        if episode >= 1000 and episode % ERROR_COUNT == 0:
            if max(judge_list) - min(judge_list) <= ERROR_RANGE:
                output = "\n  达到收敛条件，提前终止实验！\n"
                # line = [x for x in RL.choose_services]
                # line.append(reward)
                # line.append(time.time() - start)
                # line.append(episode)
                # 打印收敛结果
                # print(output)
                # print(line)
                # 记录收敛结果
                # fp = open(outfile, 'a+')
                # fp.write(output)
                # fp.write(str(line) + '\n')
                # fp.close()
                break

    print('game over')


if __name__ == "__main__":

    nodes_num, each_services_nums, all_services_nums, max_services_num = cal_num(nodeSet)
    print("1.服务节点数：{}".format(nodes_num))
    print("2.每个节点处候选子集大小：{}".format(each_services_nums))
    print("3.总的候选原子个数：{}".format(all_services_nums))
    print("4.最大候选子集个数：{}".format(max_services_num))

    update()