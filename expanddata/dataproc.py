import pymysql
# 全数据为2507

def getdata():
  conn = pymysql.connect()
  cursor = conn.cursor()
  sql = 'select RT,Avai,Thr from qws2;'
  cursor.execute(sql)
  data = cursor.fetchall()

  return data



