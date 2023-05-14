import copy

import tensorflow as tf
from tensorflow import keras
import pandas as pd
import numpy as np

class DQnetwork:
    def __init__(self, max_actions,  n_actions, n_features, epsilon, batch_size, learning_rate, gamma, replace_time, n_experience_pool):
        self.max_actions = max_actions
        self.n_actions = n_actions
        self.n_features = n_features
        self.batch_size = batch_size
        # 学习率
        self.learning_rate = learning_rate
        self.gamma = gamma
        # 贪婪度
        self.epsilon = epsilon
        # 经验池大小
        self.n_experience_pool = n_experience_pool
        # 建立经验池，n_experience_pool行，n_features*2+2列，对应s, a, r, s_
        self.experience_pool = pd.DataFrame(np.zeros([self.n_experience_pool, self.n_features * 2 + 2 + 1]))
        self.experience_pool_index = 0
        self.experience_pool_is_full = False
        # 定义两个神经网络
        self.q_pred = None
        self.q_target = None
        self.opt = tf.keras.optimizers.Adam(self.learning_rate)
        # 参数更新间隔
        self.replace_time = replace_time
        self.now_learn_time = 0

        self.e_greedy = 2e-5

    def loss_f(self, y_true, y_pred):
        return keras.losses.mse(y_true, y_pred)

    def choose_action(self, s):
        state = s
        s = np.array(s)
        s = s.reshape(1, 1)
        rand = np.random.rand()


        if rand < self.epsilon:
            # return np.random.randint(0, self.max_actions)
            return np.random.randint(0, self.n_actions[state[0]])

        else:
            self.epsilon = max(0.001, self.epsilon - self.e_greedy)
            action_value = self.q_pred.predict(np.array(s))
            return np.argmax(action_value)
            # return np.argmax(action_value[:, 0:(self.n_actions[state[0]])])

    def net_init(self):
        # q_pred
        input_features = tf.keras.Input(shape=(self.n_features), name='input_features')
        dense_0 = tf.keras.layers.Dense(32, activation='relu')(input_features)
        dense_1 = tf.keras.layers.Dense(64, activation='relu')(dense_0)
        dense_1_2 = tf.keras.layers.Dense(128, activation='relu')(dense_1)
        dense_1_1 = tf.keras.layers.Dense(256, activation='relu')(dense_1_2)
        out_put = tf.keras.layers.Dense(self.max_actions, activation='softmax', name='prediction_q_pred')(dense_1_1)
        self.q_pred = tf.keras.Model(inputs=input_features, outputs=out_put)
        # q_target
        input_features_target = tf.keras.Input(shape=(self.n_features), name='input_features_target')
        dense_0_target = tf.keras.layers.Dense(32, activation='relu')(input_features_target)
        dense_1_target = tf.keras.layers.Dense(64, activation='relu')(dense_0_target)
        dense_1_2_target = tf.keras.layers.Dense(128, activation='relu')(dense_1_target)
        dense_1_1_target = tf.keras.layers.Dense(256, activation='relu')(dense_1_2_target)
        out_put_target = tf.keras.layers.Dense(self.max_actions, activation='softmax', name='prediction_q_target')(dense_1_1_target)
        self.q_target = tf.keras.Model(inputs=input_features_target, outputs=out_put_target)

        self.q_target.set_weights(self.q_pred.get_weights())

    def net_init_LSTM(self):
        # q_pred
        input_features = tf.keras.layers.Input(shape=(None, self.n_features), name='input_features')
        lstm_1 = tf.keras.layers.LSTM(30)(input_features)
        dense_1 = tf.keras.layers.Dense(256, activation='relu')(lstm_1)
        out_put = tf.keras.layers.Dense(self.max_actions, name='prediction_q_pred')(dense_1)
        self.q_pred = tf.keras.Model(inputs=input_features, outputs=out_put)

        # q_target
        input_features_target = tf.keras.layers.Input(shape=(None, self.n_features), name='input_features_target')
        lstm_1_target = tf.keras.layers.LSTM(30)(input_features_target)
        dense_1_target = tf.keras.layers.Dense(256, activation='relu')(lstm_1_target)
        out_put_target = tf.keras.layers.Dense(self.max_actions, name='prediction_q_pred')(dense_1_target)
        self.q_target = tf.keras.Model(inputs=input_features_target, outputs=out_put_target)

        self.q_target.set_weights(self.q_pred.get_weights())

    def experience_store(self, s, a, r, s_, done):
        experience = []
        for i in range(self.n_features * 2 +2 + 1):
            if i < self.n_features:
                experience.append(s[i])
            elif self.n_features <= i < self.n_features + 1:
                experience.append(a)
            elif self.n_features + 1 <= i < self.n_features + 2:
                experience.append(r)
            elif self.n_features + 2 <= i < self.n_features * 2 + 2:
                experience.append(s_[i - self.n_features - 2])
            else:
                experience.append(done)

        self.experience_pool.loc[self.experience_pool_index] = copy.deepcopy(experience)
        self.experience_pool_index += 1
        if self.experience_pool_index == self.n_experience_pool:
            self.experience_pool_is_full = True
            self.experience_pool_index = 0

    def learn(self):
        if not self.experience_pool_is_full:
            return

        data_pool = self.experience_pool.sample(self.batch_size)

        s = np.array(data_pool.loc[:, 0: self.n_features - 1])
        a = np.array(data_pool.loc[:, self.n_features], dtype=np.int32)
        r = np.array(data_pool.loc[:, self.n_features + 1])
        s_ = np.array(data_pool.loc[:, self.n_features + 2:self.n_features * 2 + 1])
        done = np.array(data_pool.loc[:, self.n_features * 2 + 2])

        with tf.GradientTape() as Tape:
            y_pred = self.q_pred(s)
            y_target = y_pred.numpy()
            q_target = self.q_target(s_)
            q_target = q_target.numpy()
            index = np.arange(self.batch_size, dtype=np.int32)
            y_target[index, a] = r + (1 - done) * self.gamma * np.max(q_target, axis=1)
            loss_val = tf.keras.losses.mse(y_target, y_pred)
            gradients = Tape.gradient(loss_val, self.q_pred.trainable_variables)
            self.opt.apply_gradients(zip(gradients, self.q_pred.trainable_variables))

        self.now_learn_time += 1
        if self.now_learn_time == self.replace_time:
            self.replace_param()
            self.now_learn_time = 0

    def replace_param(self):
        print("replace the param")
        self.q_target.set_weights(self.q_pred.get_weights())






