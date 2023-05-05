NaNQos = [-1, 1000000, -1, -1, -1, -1, "NaN"]

def padding_data(max_num, service_data):
    for node in service_data:
        for i in range(max_num-len(node)):
            node.append(NaNQos)

    return service_data