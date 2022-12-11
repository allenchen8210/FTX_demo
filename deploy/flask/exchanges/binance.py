import ccxt
import time
from requests import Request, Session
import threading
from threading import Thread, Lock

class BinanceWrapper():
    def __init__(self):
        self.__order_info = {}
        self.__user_info = {}
        self.main_binance = ccxt.binance()
        self.main_binance.set_sandbox_mode(True)
        self.main_binance.load_markets()
        self.symbol_map = {
            "BTCUSDT": "BTC/USDT"
        }
    
    def set_order_info(self, order_info):
        self.__order_info = order_info
    
    def set_user_info(self, user_info):
        self.__user_info = user_info
    
    #def ftx_get_coins():
    #    request = Request('GET', 'https://ftx.com/api/wallet/coins')
    #    prepared = request.prepare()
    #    s = Session()
    #    response = s.send(prepared)
    #    return response.json()

    def binance_create_order(self):
        order_symbol = self.symbol_map[self.__order_info["Symbol"]]
        type = "market"  # or "limit"
        side = "buy" if self.__order_info["Strategy"] == "long" else "sell"
        #amount = 123.45  # your amount
        #price = 54.321  # your price
        #params = {
        #    'triggerPrice': 123.45,  # your stop price
        #}

        ticker = self.main_binance.fetch_ticker(order_symbol)
        last_price = ticker["last"]

        #market = self.main_binance.market(order_symbol)
        market = self.main_binance.markets[order_symbol]
        #print(market)

        #for i, user in enumerate(self.__user_info):
            # print(self.__user_info[user]["exchange"])
            # response = self.__user_info[user]["exchange"].fetch_balance()
            # print(response['total'])  # make sure you have enough futures margin...
            # print(response['info'])  # more details
            #price = 9000
            #amount = 1
            #type = 'market'  # or market
            #side = 'buy'

            #usdt_amount = self.__user_info[user]["market_info"][order_symbol]["amount"]
            #params = {
            #    #'type': 'margin',
            #    'quoteOrderQty': usdt_amount,
            #}
            #order = self.__user_info[user]["exchange"].create_order(order_symbol, type, side, amount)
            #print(order)
        #print(market["info"]["filters"])
        taker = market["taker"]    
        def launch_order(user_dict, symbol, type, side, last_price, taker):
            usdt_amount = float(user_dict["market_info"][symbol]["amount"])
            #usdt_amount = 10.0
            amount = usdt_amount / last_price
            if amount >= taker:
                print("symbol: {}, type: {}, side: {}, amount: {}"
                    .format(symbol, type, side, amount))
                order = user_dict["exchange"].create_order(symbol, type, side, amount)
                print(order)
            else:
                print("amount is too small")

        t_list = []
        for i, user in enumerate(self.__user_info):
            t_list.append(Thread(target = launch_order, 
                args=(self.__user_info[user], order_symbol, type, side, last_price, 
                taker)))
            t_list[i].start()
        for t in t_list:
            t.join()