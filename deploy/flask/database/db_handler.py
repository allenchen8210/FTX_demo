import os
import mysql.connector
import json

mysql_host = ""
if "MYSQL_HOST" in os.environ:
    mysql_host = os.environ["MYSQL_HOST"]
else:
    mysql_host = "127.0.0.1"

db = mysql.connector.connect(
  #host="172.105.242.139",
  #host="localhost",
  host=mysql_host,
  #host="mydb",
  port = 3306,
  user="root",
  password="pass",
  #password="1029*Lbx",
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
    def get_user_info(self, exchange):
        #cursor.execute("SELECT * FROM binance_user_info")
        user_info = exchange + "_user_info"
        sql = "SELECT * FROM {table_name}".format(table_name=user_info)
        cursor.execute(sql)

        result = cursor.fetchall()
        for row in result:
            user_data = {}

            if exchange == "binance":
                user_data["api_key"] = row[1]
                user_data["secret_key"] = row[2]
                user_data["market_info"] = json.loads(row[3])
                self.__user_table[row[0]] = user_data
            elif exchange == "ftx":
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

    #def set_db_user_data(self, dc_id, api_key, secret_key, ftx_sub_account, lv2_cert = "No", market_info = {}):
    #    sql = "SELECT EXISTS(SELECT * FROM user_info WHERE dc_id = %s)"
    #    id = (dc_id, )
    #    cursor.execute(sql, id)
    #    result = cursor.fetchone()
    #    ret = ""
    #    if result[0] == 1:
    #        ret = "User already exists!"
    #    else:
    #        sql = "INSERT INTO user_info (dc_id, api_key, secret_key, ftx_sub_account, lv2_cert, market_info) VALUES (%s, %s, %s, %s, %s, %s)"
    #        val = (dc_id, api_key, secret_key, ftx_sub_account, lv2_cert, json.dumps(market_info))
    #        cursor.execute(sql, val)
    #        ret = "Register success!"
    #    return ret
    
    def set_db_user_data(self, dict):

        dc_id = dict["dc_id"]
        exchange = dict["exchange"]
        user_info = exchange + "_user_info"

        sql = "SELECT EXISTS(SELECT * FROM {table_name} WHERE dc_id = %s)".format(table_name=user_info)
        val = (dc_id, )
        cursor.execute(sql, val)
        result = cursor.fetchone()
        ret = ""
        if result[0] == 1:
            ret = "User already exists!"
        else:
            if exchange == "binance":
                api_key = dict["api_key"]
                secret_key = dict["secret_key"]
                market_info = {}
                sql = "INSERT INTO {table_name} (dc_id, api_key, secret_key, market_info) VALUES (%s, %s, %s, %s)".format(table_name=user_info)
                val = (dc_id, api_key, secret_key, json.dumps(market_info))
                cursor.execute(sql, val)
                ret = "Register success!"
            elif exchange == "ftx":
                api_key = dict["api_key"]
                secret_key = dict["secret_key"]
                ftx_sub_account = dict["ftx_sub_account"]
                lv2_cert = "Yes" if dict["lv2_cert"] == "Yes" else "No"
                market_info = {}
                sql = "INSERT INTO {table_name} (dc_id, api_key, secret_key, ftx_sub_account, lv2_cert, market_info) VALUES (%s, %s, %s, %s, %s, %s)".format(table_name=user_info)
                val = (dc_id, api_key, secret_key, ftx_sub_account, lv2_cert, json.dumps(market_info))
                cursor.execute(sql, val)
                ret = "Register success!"
        return ret

    def set_db_market_info_amount(self, id, market):
        user_info = market["exchange"] + "_user_info"
        symbol = market["symbol"]
        amount = market["amount"]
        sql = "SELECT market_info FROM {table_name} WHERE dc_id = %s".format(table_name=user_info)
        val = (id, )
        cursor.execute(sql, val)
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
            info[symbol] = {}
            markets = info
        else:
            markets = json.loads(markets)
            if symbol not in markets.keys():
                markets[symbol] = {}
        markets[symbol]["amount"] = amount

        sql_update = "UPDATE {table_name} SET market_info = %s WHERE dc_id = %s".format(table_name=user_info)
        cursor.execute(sql_update, (json.dumps(markets), id, ))

    def set_lv2_cert(self, id, enable):
        sql = "UPDATE {table_name} SET lv2_cert = %s WHERE dc_id = %s".format(table_name=user_info)
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