from dataproc import getdata

class StepCal:
    def __init__(self, n_states):
        self.service_data = getdata()
        self.n_states = n_states

    def get_max_rt(self):
        max = 0.0
        for i in range(len(self.service_data)):
            for num in range(len(self.service_data[i])):
                if(self.service_data[i][num][1] > max):
                    max = self.service_data[i][num][1]

        return max


    def get_min_rt(self):
        min = 10000000.0
        for i in range(len(self.service_data)):
            for num in range(len(self.service_data[i])):
                if (self.service_data[i][num][1] < min):
                    min = self.service_data[i][num][1]

        return min


    def get_max_avai(self):
        max = 0.0
        for i in range(len(self.service_data)):
            for num in range(len(self.service_data[i])):
                if (self.service_data[i][num][2] > max):
                    max = self.service_data[i][num][2]

        return max

    def get_min_avai(self):
        min = 10000000.0
        for i in range(len(self.service_data)):
            for num in range(len(self.service_data[i])):
                if (self.service_data[i][num][2] < min):
                    min = self.service_data[i][num][2]

        return min

    def get_max_thr(self):
        max = 0.0
        for i in range(len(self.service_data)):
            for num in range(len(self.service_data[i])):
                if (self.service_data[i][num][3] > max):
                    max = self.service_data[i][num][3]

        return max

    def get_min_thr(self):
        min = 10000000.0
        for i in range(len(self.service_data)):
            for num in range(len(self.service_data[i])):
                if (self.service_data[i][num][3] < min):
                    min = self.service_data[i][num][3]

        return min

    def get_max_succ(self):
        max = 0.0
        for i in range(len(self.service_data)):
            for num in range(len(self.service_data[i])):
                if (self.service_data[i][num][4] > max):
                    max = self.service_data[i][num][4]

        return max

    def get_min_succ(self):
        min = 10000000.0
        for i in range(len(self.service_data)):
            for num in range(len(self.service_data[i])):
                if (self.service_data[i][num][4] < min):
                    min = self.service_data[i][num][4]

        return min

    def get_max_reli(self):
        max = 0.0
        for i in range(len(self.service_data)):
            for num in range(len(self.service_data[i])):
                if self.service_data[i][num][5] > max:
                    max = self.service_data[i][num][5]

        return max

    def get_min_reli(self):
        min = 10000000.0
        for i in range(len(self.service_data)):
            for num in range(len(self.service_data[i])):
                if self.service_data[i][num][5] < min:
                    min = self.service_data[i][num][5]

        return min

    def receive(self, state, action):
        # 如果为无效行为
        if action >= len(self.service_data[state]):
            return -1

        maxTime = self.get_max_rt()
        minTime = self.get_min_rt()
        maxAvail = self.get_max_avai()
        minAvail = self.get_min_avai()
        maxReli = self.get_max_reli()
        minReli = self.get_min_reli()
        maxSucc = self.get_max_succ()
        minSucc = self.get_min_succ()
        maxThrou = self.get_max_thr()
        minThrou = self.get_min_thr()
        r = self.service_data[state][action]
        f1 = ((r[1] - minTime) / (maxTime - minTime))+ \
            ((maxAvail - r[2]) / (maxAvail - minAvail))+ \
            ((maxThrou - r[3]) / (maxThrou - minThrou))+ \
            ((maxSucc - r[4]) / (maxSucc - minSucc))
        f = 1.0 / 4 * f1
        return f

    def step(self, s, actions):  # 根据选择行为计算reward
        # 此状态为终状态
        if s == self.n_states - 1:
            done = True
            s_ = -1
            f = 0
            # 计算Qos评分
            for state in range(len(actions)):
                # print(state, actions[state])
                if self.receive(state, actions[state]) == -1:
                    f = -1
                    break
                f += self.receive(state, actions[state])  # 传state和action
            reward = self.receive(s, actions[s])
        # 此状态不为终状态
        else:
            done = False
            s_ = s + 1
            reward = self.receive(s, actions[s])

        return s_, reward, done

    def get_id_list(self, action_list):
        id_list = []
        for i in range(len(action_list)):
            id_list.append([self.service_data[i][action_list[i]][0], self.service_data[i][action_list[i]][6]])

        return id_list