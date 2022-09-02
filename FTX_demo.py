
import hmac
from unittest import result
from requests import Request, Session
import schedule
import time
import requests
from bs4 import BeautifulSoup
import json
import datetime
from datetime import datetime


API_key = "2CTaC7wxb1s56GTqukpDejOv61cERvytogaX9-WF"
API_secret = "ivMsSl-FhkaamavhklAS34pLDbyheONGbfsHAPyw"


#API_secret = "T4lPid48QtjNxjLUFOcUZghD7CUJ7sTVsfuvQZF2"
#API_key = "LR0RQT6bKjrUNh38eCw9jYC89VDAbRkCogAc_XAm"
request = Request('GET', 'https://otc.ftx.com/api/time')
prepared = request.prepare()

s = Session()

response = s.send(prepared)
FTX_server_time = response.json()['result']
print(FTX_server_time)
# input datetime
year = int(FTX_server_time[0:4])
month = int(FTX_server_time[5:7])
day = int(FTX_server_time[8:10])
hour = int(FTX_server_time[11:13])
min = int(FTX_server_time[14:16])
sec = int(FTX_server_time[17:19])
print(year, month, day, hour, min, sec)
dt = datetime(year, month, day, hour, min, sec)
# epoch time
epoch_time = datetime(1970, 1, 1)

# subtract Datetime from epoch datetime
delta = (dt - epoch_time)
delta = delta.total_seconds()
ts = delta*1000
print(ts)
print(time.time() * 1000)

ts = int(time.time() * 1000)
request = Request('GET', 'https://ftx.com/api/wallet/balances')
prepared = request.prepare()
signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
signature = hmac.new(API_secret.encode(), signature_payload, 'sha256').hexdigest()

print(signature_payload)
print(signature)

request.headers[f'FTX-KEY'] = API_key
request.headers[f'FTX-SIGN'] = signature
request.headers[f'FTX-TS'] = str(ts)

s = Session()
response = s.send(prepared)
print(response.json())

#url = 'https://ftx.com/api/markets'
#list_req = requests.get(url)
#soup = BeautifulSoup(list_req.content, "html.parser")
#getjson = json.loads(soup.text)
#print(getjson['result'])



