import sys
args = sys.argv[1:]
if len(args) > 0:
    sys.path.append(args[1])
from flask import request
from flask import Flask
from requests import Request, Session
import json
import database
import exchanges
import ccxt
import time
#import multiprocessing as mp
#from multiprocessing import Process, Manager
import threading
from threading import Thread, Lock
import os

FTX_SUB_ACCOUNT = "test1"

"""
YOUR_API_KEY = "2CTaC7wxb1s56GTqukpDejOv61cERvytogaX9-WF"
YOUR_API_SECRET = "ivMsSl-FhkaamavhklAS34pLDbyheONGbfsHAPyw"

ftx = ccxt.ftx({
    'apiKey': YOUR_API_KEY,
    'secret': YOUR_API_SECRET,
    'enableRateLimit': True,
})
"""

#fetchkey = database.FetchKey("imugly1029@gmail.com")
#apikey = fetchkey.get_apikey()
#secretkey = fetchkey.get_secretkey()
lock = Lock()

class Handler():
    def __init__(self):
        self.p_list = []
        self.__order_info = {}
        self.__user_info = {}
        self.exchange_config = exchanges.FTXWrapper()
        self.db = database.DBHandler()
    def set_order_info(self, order_info):
        self.__order_info = order_info
    def set_user_info(self, user_info):
        self.__user_info = user_info
    def get_order_info(self):
        return self.__order_info
    def get_user_info(self):
        return self.__user_info
    def fetch_user_info(self):
        while True:
            lock.acquire()
            user_info = self.db.get_user_info()
            for info in user_info.values():
                info["exchange"] = ccxt.ftx({
                    'headers':{
                        'FTX-SUBACCOUNT': info["ftx_sub_account"]
                    },
                    'apiKey': info["api_key"],
                    'secret': info["secret_key"],
                    #'options': {
                    #    'defaultType': 'future',  # -------------- quotes and 'future'
                    #},
                })
            self.set_user_info(user_info)
            lock.release()
            time.sleep(1)

    def set_exchange_config(self, order_info, user_info):
        self.exchange_config.set_order_info(order_info)
        self.exchange_config.set_user_info(user_info)

    def set_db_user_data(self, dict):
        dc_id = dict["dc_id"]
        api_key = dict["api_key"]
        secret_key = dict["secret_key"]
        ftx_sub_account = dict["ftx_sub_account"]
        lv2_cert = "Yes" if dict["lv2_cert"] == "Yes" else "No"
        lock.acquire()
        self.db.set_db_user_data(dc_id, api_key, secret_key, ftx_sub_account, lv2_cert)
        lock.release()

    def set_db_market_info(self, dict):
        dc_id = dict["dc_id"]
        for market in dict["markets"]:
            if "amount" in market.keys():
                #print(market.keys())
                lock.acquire()
                self.db.set_db_market_info_amount(dc_id, market["symbol"], market["amount"])
                lock.release()

handler = Handler()

app = Flask(__name__)
@app.route("/orderFTX", methods=['GET', 'POST'])
def api_orderFTX():
    if request.method=='POST':
        #begin = time.time()
        #lock.acquire()
        #print(json.dumps(request.get_json(), indent=1)) # JSON object
        #handler.order_info = json.loads(json.dumps(request.get_json(), indent=1)) # Dictionary object
        handler.set_order_info(json.loads(json.dumps(request.get_json(), indent=1)))

        order_info = dict(handler.get_order_info())
        user_info = dict(handler.get_user_info())
        #print(order_info)
        #print(user_info["547083804150464513"]["market_info"])
        #print(user_info["547083804150464513"])

        handler.set_exchange_config(order_info, user_info)
        handler.exchange_config.ftx_create_order()
        #end = time.time()
        #print("{} s".format(end - begin))
        #lock.release()
        return "OK this is a post method"
    else:
        return ("OK!")

@app.route("/registerUser", methods=['GET', 'POST'])
def api_registerUser():
    if request.method=='POST':
        handler.set_db_user_data(json.loads(json.dumps(request.get_json(), indent=1)))
        return "Register success!"

@app.route("/updateMarketInfo", methods=['GET', 'POST'])
def api_updateMarketInfo():
    if request.method=='POST':
        handler.set_db_market_info(json.loads(json.dumps(request.get_json(), indent=1)))
        return "Update success!"

@app.route("/FTX_fetch_positions")
def FTX_fetch_positions(): 
    try: 
        #print(request.args['apiKey'])
        dict = json.loads(json.dumps(request.get_json(), indent=1))

        ftx = ccxt.ftx({
            'headers':{
                'FTX-SUBACCOUNT': dict["FTX-SUBACCOUNT"]
            },
            'apiKey': dict["apiKey"],
            'secret': dict["secret"],
            'enableRateLimit': True,
        })
        symbols = ftx.load_markets()
        #print(symbols)
        print(ftx.fetch_ticker("BTC/USDT"))

        quote = ftx.fetch_balance() # fetch FTX balance, requires authentication.
        return (json.dumps(quote))
    except:
        return ("Authentication Fail")

if __name__ == '__main__':
    t_list = []
    t_list.append(Thread(target=handler.fetch_user_info))
    for t in t_list:
        t.start()
    app.run()
    for t in t_list:
        t.join()

"""
{
    "Name":"Exponential Bollinger Bands",
    "Exchange":"BINANCE",
    "Symbol":"BTCUSDT",
    "Currency":"USDT",
    "Price":"20000.00",
    "Strategy":"long"
}
"""



"""
@app.route("/hello")
def api_hello():
    if 'name' in request.args:
        return 'Hello '+ request.args['name']+"\n"
    else:
        return 'Hello John Doe\n'

@app.route("/orderFTX")
def api_orderFTX():
    if 'op' in request.args and 'amount' in request.args and 'price' in request.args:
        return request.args['op']+' price='+request.args['price']+ ' amount='+request.args['amount']+"\n"
    elif 'op' in request.args:
        return request.args['op']+'\n'
    else:
        return 'error please fill proper attri\n'


@app.route("/getFTXCoins")
def api_getFTXCoins():
    print("====getFTXCoins====")
    return getFTXCoins()


def getFTXCoins():
    request = Request('GET', 'https://ftx.com/api/wallet/coins')
    prepared = request.prepare()
    s = Session()
    response = s.send(prepared)
    return response.json()

@app.route("/FTX_fetch_positions")
def FTX_fetch_positions(): 

   try: 
        quote = ftx.fetch_balance() # fetch FTX balance, requires authentication.
        return (json.dumps(quote))
   except:
        return ("Authentication Fail")
"""

