

def readNodeSet(nodeSet):
    fd = open(nodeSet, 'r')
    nodeSets = fd.readlines()[1]  # str
    nodeSets = nodeSets.split(' ')  # list
    each_services_num = []
    for node in nodeSets:
        each_services_num.append(int(node))

    all_services_num = sum(each_services_num)
    node_num = len(each_services_num)
    max_servise_num = max(each_services_num)

    return node_num, each_services_num, all_services_num, max_servise_num