import os

import psycopg2
import psycopg2.extras
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch

es = Elasticsearch(os.environ.get('ingest', 'elastic-service'))

con = psycopg2.connect(user = "postgres",
                  password = "heri7777",
                  host = "64.227.72.33",
                  port = "9700",
                  database = "postgres")
                  
                 
dict_cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
#cur = con.cursor()


def getproduct():
  offset = 0
  limit = 500
  
#     while True:
  
#     dict_cur.execute("select * from toko OFFSET {} LIMIT {}".format(offset, limit))
  dict_cur.execute("select * from toko")

#         datas = dict_cur.fetchall()
#         if len(datas) <= 0:
#             break

  for data in dict_cur:
    data = dict(data)
    #yield data
    print(data['shopid'])
    yield  {
       "_index": "toko",
       "_id": data['shopid'],
       "_source": data
    }
    
    #cur.execute('DELETE FROM product WHERE itemid = %s;', (data['itemid'],))
     

     
datas = getproduct()

while True:
  payload = []
  try:
    for c in range(0, 500):
      payload.append(next(datas))

  except StopIteration as e:
    bulk(es, payload)
    break


  bulk(es, payload)
  
  
  
  
  
  