from dataproc import getdata

service_data = getdata()

def get_max_rt():
    max = 0.0
    for i in range(len(service_data)):
        for num in range(len(service_data[i])):
            if(service_data[i][num][1] > max):
                max = service_data[i][num][1]

    return max


def get_min_rt():
    min = 10000000.0
    for i in range(len(service_data)):
        for num in range(len(service_data[i])):
            if (service_data[i][num][1] < min):
                min = service_data[i][num][1]

    return min


def get_max_avai():
    max = 0.0
    for i in range(len(service_data)):
        for num in range(len(service_data[i])):
            if (service_data[i][num][2] > max):
                max = service_data[i][num][2]

    return max

def get_min_avai():
    min = 10000000.0
    for i in range(len(service_data)):
        for num in range(len(service_data[i])):
            if (service_data[i][num][2] < min):
                min = service_data[i][num][2]

    return min

def get_max_thr():
    max = 0.0
    for i in range(len(service_data)):
        for num in range(len(service_data[i])):
            if (service_data[i][num][3] > max):
                max = service_data[i][num][3]

    return max

def get_min_thr():
    min = 10000000.0
    for i in range(len(service_data)):
        for num in range(len(service_data[i])):
            if (service_data[i][num][3] < min):
                min = service_data[i][num][3]

    return min

def get_max_succ():
    max = 0.0
    for i in range(len(service_data)):
        for num in range(len(service_data[i])):
            if (service_data[i][num][4] > max):
                max = service_data[i][num][4]

    return max

def get_min_succ():
    min = 10000000.0
    for i in range(len(service_data)):
        for num in range(len(service_data[i])):
            if (service_data[i][num][4] < min):
                min = service_data[i][num][4]

    return min

def get_max_reli():
    max = 0.0
    for i in range(len(service_data)):
        for num in range(len(service_data[i])):
            if service_data[i][num][5] > max:
                max = service_data[i][num][5]

    return max

def get_min_reli():
    min = 10000000.0
    for i in range(len(service_data)):
        for num in range(len(service_data[i])):
            if service_data[i][num][5] < min:
                min = service_data[i][num][5]

    return min

def receive(service):
    maxTime = get_max_rt()
    minTime = get_min_rt()
    maxAvail = get_max_avai()
    minAvail = get_min_avai()
    maxReli = get_max_reli()
    minReli = get_min_reli()
    maxSucc = get_max_succ()
    minSucc = get_min_succ()
    maxThrou = get_max_thr()
    minThrou = get_min_thr()
    r = service
    f1 = ((r[1] - minTime) / (maxTime - minTime))+ \
        (-(r[2] - minAvail) / (maxAvail - minAvail))+ \
        (-(r[3] - minThrou) / (maxThrou - minThrou))+ \
        (-(r[4] - minSucc) / (maxSucc - minSucc))+ \
        (-(r[5] - minReli) / (maxReli - minReli))
    f = -1.0 / 6 * f1
    return f