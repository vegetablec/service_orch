import pymysql
# 全数据为2507

def getdata():
  conn = pymysql.connect(host='42.193.113.93', user='root', password='291482jX', db='qws')
  cursor = conn.cursor()
  sql = 'select RT,Avai,Thr from qws2;'
  cursor.execute(sql)
  data = cursor.fetchall()

  return data



