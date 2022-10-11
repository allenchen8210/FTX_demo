import os
import mysql.connector
import json

db = mysql.connector.connect(
  #host="172.105.242.139",
  #host="localhost",
  #host="127.0.0.1",
  host="mydb",
  port = 3306,
  user="root",
  password="pass",
  database="test2",
  autocommit=True
)
cursor = db.cursor(buffered=True)

# 查找已存在的 db
#cursor.execute("SHOW DATABASES")
#for x in cursor:
    #print(x)
# 創建 db: test2
#cursor.execute("CREATE DATABASE test2")
# 創建 table: user_info
#cursor.execute("CREATE TABLE user_info (dc_id VARCHAR(255), api_key VARCHAR(255), secret_key VARCHAR(255))")


#sql = f"SELECT {col_str} FROM {table_name} WHERE {condition};"
#cursor = cursor.execute(sql)

#cursor.fetchone()
#for c in cursor:
#	print(c)

class DBHandler():
    def __init__(self):
        self.__user_table = {}
    def get_user_info(self):
        cursor.execute("SELECT * FROM user_info")
        result = cursor.fetchall()
        for row in result:
            user_data = {}
            user_data["api_key"] = row[1]
            user_data["secret_key"] = row[2]
            user_data["ftx_sub_account"] = row[3]
            user_data["lv2_cert"] = row[4]
            user_data["market_info"] = json.loads(row[5])
            self.__user_table[row[0]] = user_data

        # Fake data
        #data = self.__user_table['547083804150464513']
        #for i in range(0, 10):
        #    self.__user_table[str(int('547083804150464513') + i)] = data

        return self.__user_table

    def set_db_user_data(self, dc_id, api_key, secret_key, ftx_sub_account, lv2_cert = "No", market_info = {}):
        sql = "INSERT INTO user_info (dc_id, api_key, secret_key, ftx_sub_account, lv2_cert, market_info) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (dc_id, api_key, secret_key, ftx_sub_account, lv2_cert, json.dumps(market_info))
        cursor.execute(sql, val)

    def set_db_market_info_amount(self, id, market, params):
        sql = "SELECT market_info FROM user_info WHERE dc_id = %s"
        dc_id = (id, )
        cursor.execute(sql, dc_id)
        result = cursor.fetchone()
        #print(result[0])
        #result = cursor.fetchall()
        #for r in result:
        #    print(r)

        #markets = json.loads(json.dumps(result[0]))
        markets = result[0]
        #print(json.dumps(result[0]))
        #print(json.loads(json.dumps(result[0])))
        #markets = {'ETHUSDT': {'amount': 50}}
        if markets is None:
            info = {}
            info[market] = {}
            markets = info
        else:
            markets = json.loads(markets)
            if market not in markets.keys():
                markets[market] = {}
        markets[market]["amount"] = params

        sql_update = "UPDATE user_info SET market_info = %s WHERE dc_id = %s"
        cursor.execute(sql_update, (json.dumps(markets), id, ))

    def set_lv2_cert(self, id, enable):
        sql = "UPDATE user_info SET lv2_cert = %s WHERE dc_id = %s"
        cursor.execute(sql, (enable, id, ))
        return

"""
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# 引用私密金鑰
# path/to/serviceAccount.json 請用自己存放的路徑
sak = os.path.abspath(os.path.dirname(__file__)) + "/serviceAccountKey.json"
cred = credentials.Certificate(sak)

# 初始化firebase，注意不能重複初始化
firebase_admin.initialize_app(cred)

# 初始化firestore
db = firestore.client()

class FetchKey():
    def __init__(self, email):
        #print("email: {}".format(email))
        self.email = email
        self.docs = db.collection("User").stream()
        for doc in self.docs:
            if self.email == doc.to_dict()['email']:
                self.data_dict = doc.to_dict()
                self.id = doc.id
                self.apikey = self.data_dict['apikey']
                self.secretkey = self.data_dict['secretkey']
    def get_apikey(self):
        return self.apikey
    def get_secretkey(self):
        return self.secretkey
"""