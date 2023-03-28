import pymysql
import random

conn = pymysql.connect(host='42.193.113.93', user='root', password='291482jX', db='qws')
cursor = conn.cursor()
sql = 'select id,RT,Avai,Thr,Succ,Name from qws2;'
cursor.execute(sql)
data = cursor.fetchall()
nodedata = []
for i in range(0,10):
  nodedata.append(random.sample(data, random.randint(1, 1000)))

