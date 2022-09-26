import ccxt
import time
from requests import Request, Session
import threading
from threading import Thread, Lock

class FTXWrapper():
    def __init__(self):
        self.__order_info = {}
        self.__user_info = {}
        self.symbol_map = {"BTCUSDT": "BTC/USDT"}
    
    def set_order_info(self, order_info):
        self.__order_info = order_info
    
    def set_user_info(self, user_info):
        self.__user_info = user_info
    
    def ftx_get_coins():
        request = Request('GET', 'https://ftx.com/api/wallet/coins')
        prepared = request.prepare()
        s = Session()
        response = s.send(prepared)
        return response.json()

    def ftx_create_order(self):
        #symbol = self.symbol_map[self.__order_info["Symbol"]]
        type = "market"  # or "limit"
        side = "buy" if self.__order_info["Strategy"] == "long" else "sell"
        #amount = 123.45  # your amount
        #price = 54.321  # your price
        #params = {
        #    'triggerPrice': 123.45,  # your stop price
        #}
        
        def launch_order(user_dict, symbol, type, side):
            amount = user_dict["market_info"][symbol]["amount"]
            symbol = self.symbol_map[symbol]
            print("symbol: {}, type: {}, side: {}, amount: {}"
                .format(symbol, type, side, amount))
            #order = user_dict["exchange"].create_order(symbol, type, side, amount)
            #print(order)
        
        t_list = []
        for i, user in enumerate(self.__user_info):
            t_list.append(Thread(target=launch_order, 
                args=(self.__user_info[user], self.__order_info["Symbol"], type, side)))
            t_list[i].start()
        for t in t_list:
            t.join()
