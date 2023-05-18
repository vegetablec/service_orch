import numpy as np
import csv
from keras.models import Sequential
from keras.layers import Conv1D, Flatten, Dense
from keras.models import load_model
from keras.utils.vis_utils import plot_model
from dataproc import getdata
Train = True
Test = True
# 准备数据
def readdata(url):
    with open(url, 'r', newline='') as file:
        reader = csv.DictReader(file)
        data = []
        for row in reader:
            onedata = []
            onedata.append(float(row['RT']))
            onedata.append(float(row['Avai']))
            onedata.append(float(row['Thr']))
            onedata.append(float(row['Late']))
            onedata.append(int(row['Place']))
            onedata.append(float(row['Label']))
            data.append(onedata)
        i = 0
        train_x = []
        train_y = []
        test_x = []
        test_y = []
        while i < len(data):
            if i >= 0.9*len(data):
                test_x.append(data[i][0:5])
                test_y.append(data[i][5])
            else:
                train_x.append(data[i][0:5])
                train_y.append(data[i][5])
            i += 1
    return np.array(train_x), np.array(train_y), np.array(test_x), np.array(test_y)

train_x, train_y, test_x, test_y = readdata("traindata_label.csv")
#print(train_x)
# print(train_y)
# print(test_x)
# print(test_y)
if Train:
# 构建CNN模型
    model = Sequential()
    model.add(Conv1D(32, 3, activation='relu', input_shape=(5, 1)))  # 一维卷积层
    model.add(Flatten())  # 扁平化层
    model.add(Dense(48, activation='relu'))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(12, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))  # 输出层
    #plot_model(model, to_file='model.png', show_shapes=True)
    # 编译和训练模型
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(np.expand_dims(train_x, axis=2), train_y, epochs=10, batch_size=32)
    model.save('model.h5')
    plot_model(model, to_file='cnn_model.jpg', show_shapes=True, show_dtype=True, show_layer_names=True)
# 使用训练好的模型进行评分

if Test:
    model = load_model('model.h5')
    # print(test_x)
    print(np.expand_dims(test_x, axis=2))
    scores = model.predict(np.expand_dims(test_x, axis=2))
    for i in range(len(test_y)):
        print((test_y[i]-scores[i])/test_y[i])
    #print(scores)