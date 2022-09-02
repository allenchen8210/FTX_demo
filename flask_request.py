
from flask import request
from flask import Flask
from requests import Request, Session
import json
import ccxt



YOUR_API_KEY = "2CTaC7wxb1s56GTqukpDejOv61cERvytogaX9-WF"
YOUR_API_SECRET = "ivMsSl-FhkaamavhklAS34pLDbyheONGbfsHAPyw"

ftx = ccxt.ftx({
    'apiKey': YOUR_API_KEY,
    'secret': YOUR_API_SECRET,
    'enableRateLimit': True,
})




app = Flask(__name__)
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



@app.route("/orderFTXByJson", methods=['GET', 'POST'])
def api_orderFTXByJson():
    if request.method=='POST':
        #print(request.get_json())
        print(json.dumps(request.get_json(), indent=1))

        return "OK this is a post method"
    else:
        return ("OK!")

@app.route("/FTX_fetch_positions")
def FTX_fetch_positions(): 

   try: 
        quote = ftx.fetch_balance() # fetch FTX balance, requires authentication.
        return (json.dumps(quote))
   except:
        return ("Authentication Fail")


