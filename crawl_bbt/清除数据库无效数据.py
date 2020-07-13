import pymysql

conn = pymysql.connect(host='120.92.164.236', port=3306, user='tbb', password='bbttbb139', db='bbt')
cur = conn.cursor()
cur.execute('use bbt')
cur.execute('select GOODS_ID from goods_detail where isnull(BIG_IMG1)')
data = cur.fetchall()
for i in data:
    cur.execute('delete  from goods_detail where GOODS_ID= %s ', (i[0]))
conn.commit()

conn.close()
cur.close()