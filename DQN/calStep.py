from dataproc import getdata

class StepCal:
    def __init__(self, n_states, actions):
        self.service_data = getdata(n_states, actions)
        self.n_states = n_states
        self.maxRT = 0
        self.minRT = 0
        self.maxAvai = 0
        self.minAvai = 0
        self.maxThr = 0
        self.minThr = 0
        self.maxLate = 0
        self.minLate = 0

    def getMaxandMin(self):
        self.maxTime = self.get_max_rt()
        self.minTime = self.get_min_rt()
        self.maxAvail = self.get_max_avai()
        self.minAvail = self.get_min_avai()
        self.maxThrou = self.get_max_thr()
        self.minThrou = self.get_min_thr()
        self.maxLate = self.get_max_late()
        self.minLate = self.get_min_late()

    def get_max_rt(self):
        max = 0.0
        for i in range(len(self.service_data)):
            for num in range(len(self.service_data[i])):
                if(self.service_data[i][num][0] > max):
                    max = self.service_data[i][num][0]

        return max


    def get_min_rt(self):
        min = 10000000.0
        for i in range(len(self.service_data)):
            for num in range(len(self.service_data[i])):
                if (self.service_data[i][num][0] < min):
                    min = self.service_data[i][num][0]

        return min


    def get_max_avai(self):
        max = 0.0
        for i in range(len(self.service_data)):
            for num in range(len(self.service_data[i])):
                if (self.service_data[i][num][1] > max):
                    max = self.service_data[i][num][1]

        return max

    def get_min_avai(self):
        min = 10000000.0
        for i in range(len(self.service_data)):
            for num in range(len(self.service_data[i])):
                if (self.service_data[i][num][1] < min):
                    min = self.service_data[i][num][1]

        return min

    def get_max_thr(self):
        max = 0.0
        for i in range(len(self.service_data)):
            for num in range(len(self.service_data[i])):
                if (self.service_data[i][num][2] > max):
                    max = self.service_data[i][num][2]

        return max

    def get_min_thr(self):
        min = 10000000.0
        for i in range(len(self.service_data)):
            for num in range(len(self.service_data[i])):
                if (self.service_data[i][num][2] < min):
                    min = self.service_data[i][num][2]

        return min

    def get_max_late(self):
        max = 0.0
        for i in range(len(self.service_data)):
            for num in range(len(self.service_data[i])):
                if (self.service_data[i][num][3] > max):
                    max = self.service_data[i][num][3]

        return max

    def get_min_late(self):
        min = 10000000.0
        for i in range(len(self.service_data)):
            for num in range(len(self.service_data[i])):
                if (self.service_data[i][num][3] < min):
                    min = self.service_data[i][num][3]

        return min


    def receive(self, state, action):
        # 如果为无效行为
        if action >= len(self.service_data[state]):
            return -1

        r = self.service_data[state][action]
        f1 = ((self.maxTime - r[0]) / (self.maxTime - self.minTime))+ \
            ((r[1] - self.minAvail) / (self.maxAvail - self.minAvail))+ \
            ((r[2] - self.minThrou) / (self.maxThrou - self.minThrou))+ \
            ((self.maxLate - r[3]) / (self.maxLate - self.minLate))
        f = 1.0 / 4 * f1
        return f

    def step(self, s, actions):  # 根据选择行为计算reward
        # 此状态为终状态
        if s == self.n_states - 1:
            done = True
            s_ = -1
            f = 0
            # 计算Qos评分
            reward = self.receive(s, actions[s])
        # 此状态不为终状态
        else:
            done = False
            s_ = s + 1
            reward = self.receive(s, actions[s])

        return s_, reward, done
