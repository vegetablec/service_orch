import pymysql
# 全数据为2507

def getdata():
  conn = pymysql.connect(host='42.193.113.93', user='root', password='291482jX', db='qws')
  cursor = conn.cursor()
  sql = 'select id,RT,Avai,Thr,Succ,Reli,Name from qws2;'
  cursor.execute(sql)
  data = cursor.fetchall()
  nodeSet_file = "nodeSet_1.txt"
  # print(len(list(data)))
  fd = open(nodeSet_file, 'r')
  nodeSets = fd.readlines()[1]  # str
  nodeSets = nodeSets.split(' ')  # list
  # print(nodeSets)
  nodedata = []
  # for i in range(0, 10):
  #   nodedata.append([])
  #   _num = int(nodeSets[i])
  #   for num in range(_num):
  #     nodedata[i].append(data[_num % 2507])
  #     _num += _num
  for i in range(0, 10):
    nodedata.append([])
    for j in range(50):
        nodedata[i].append(data[i*50+j])

  return nodedata



