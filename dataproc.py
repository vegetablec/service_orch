import pymysql
import random

conn = pymysql.connect(host='42.193.113.93', user='root', password='291482jX', db='qws')
cursor = conn.cursor()
sql = 'select id,RT,Avai,Thr,Succ,Name from qws2;'
cursor.execute(sql)
data = []
data = cursor.fetchall()
print(data)
random.shuffle(data)
print(data)

