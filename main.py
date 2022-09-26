"""
from flask import request
from flask import Flask
from requests import Request, Session
import json
import ccxt
import database
import sys



class EndpointAction(object):

    def __init__(self, action):
        self.action = action

    def __call__(self, *args):
        # Perform the action
        answer = self.action()
        # Create the answer (bundle it in a correctly formatted HTTP answer)
        self.response = flask.Response(answer, status=200, headers={})
        # Send it
        return self.response

class TradingViewBot(object):

    def add_all_endpoints(self):
        # Add root endpoint
        self.add_endpoint(endpoint="/", endpoint_name="/", handler=self.action)
        # Add action endpoints
        self.add_endpoint(endpoint="/add_X", endpoint_name="/add_X", handler=self.add_X)

        self.add_endpoint(endpoint="/orderFTXByJson", endpoint_name="/orderFTXByJson", handler=self.api_orderFTXByJson)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler)) 
        # You can also add options here : "... , methods=['POST'], ... "

    # ==================== ------ API Calls ------- ====================
    def action(self):
        # Dummy action
        return "action" # String that will be returned and display on the webpage
        # Test it with curl 127.0.0.1:5000
    def add_X(self):
        # Dummy action
        return "add_X"
        # Test it with curl 127.0.0.1:5000/add_X
    
    def api_orderFTXByJson():
        if request.method=='POST':
            #print(request.get_json())
            print(json.dumps(request.get_json(), indent=1))

            return "OK this is a post method"
        else:
            return ("OK!")



if __name__ == '__main__':
    bot = TradingViewBot('wrap')
    #bot.add_endpoint(endpoint='/ad', endpoint_name='ad', handler=action)
    bot.run()
"""