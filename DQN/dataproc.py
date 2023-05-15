import pymysql
# 全数据为2507

def getdata(nodenum, servicenum):
  conn = pymysql.connect()
  cursor = conn.cursor()
  sql = 'select RT,Avai,Thr,Late,Place from data;'
  cursor.execute(sql)
  data = cursor.fetchall()
  nodedata = []
  for i in range(0, 20):
    nodedata.append([])
    for j in range(500):
        nodedata[i].append(list(data[i*500+j]))

  return nodedata



