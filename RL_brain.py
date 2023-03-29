import numpy as np
import pandas as pd

from getscore import receive

class QLearningTable:
    def __init__(self, n_states, each_services_nums, max_services_num, learning_rate, reward_decay,
                 e_greedy, e_greedy_increment=0.01):
        self.each_services_nums = each_services_nums
        self.n_actions = max_services_num
        self.n_states = n_states
        self.lr = learning_rate
        self.gamma = reward_decay
        self.choose_services = [0 for i in range(self.n_states)]
        self.epsilon_max = e_greedy
        self.epsilon_increment = e_greedy_increment
        self.epsilon = 0 if e_greedy_increment is not None else self.epsilon_max

        # 生成Q表，无效部分为NaN
        services_tmp_list = [[0] * self.each_services_nums[i] for i in range(len(each_services_nums))]
        self.q_table = pd.DataFrame(
            services_tmp_list,
            columns=list(range(self.n_actions)))

    def choose_action(self, state):  # 选择动作
        state_action = self.q_table.loc[state, :self.each_services_nums[state]]  # 取Q表中有效部分切片
        # 选择随机行为
        if (np.random.uniform() > self.epsilon) or ((state_action == 0).all()):
            action = np.random.choice(list(range(self.each_services_nums[state])))

        # 选择最大价值行为，相同价值行为随机选择
        else:
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        self.choose_services[state] = action
        return action

    def learn(self, s, a, r, s_):  # 更新Q表
        q_predict = self.q_table.loc[s, a]
        # 下一状态不结束
        if s_ != -1:
            q_target = r + self.gamma * self.q_table.loc[s_, :self.each_services_nums[s_]].max()
        # 下一状态结束
        else:
            q_target = r
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)

    def step(self, s, a):  # 根据选择行为计算reward
        # 此状态为终状态
        if s == self.n_states - 1:
            done = True
            s_ = -1
            # 计算Qos评分
            f = receive(s, a)  # 传state和action
            reward = f
        # 此状态不为终状态
        else:
            done = False
            s_ = s + 1
            reward = 0

        return s_, reward, done