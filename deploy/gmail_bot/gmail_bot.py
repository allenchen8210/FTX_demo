from email_reader import getEmails
import json
import threading
from threading import Thread, Lock
import requests

class Handler():
    def __init__(self):
        self.newest_email_date = ""
        self.last_email_date = ""
        self.order_info = {}
        self.sender = "TradingView <noreply@tradingview.com>"
        self.subject = "快訊： EBB (ohlc4, 21, 0, 2)：任何alert()函數調用"
        #self.webhook_url = "http://127.0.0.1:5000/orderFTX"
        self.webhook_url = "http://myapp:5000/orderFTX"
    def get_emails(self):
        #webhook_url = 'https://webhook.site/feefe4c4-55c7-4b93-acfd-f348e2fd3e79'
        #webhook_url = 'http://127.0.0.1:5000/webhook'
        #data = { 'name': 'This is an example for webhook blablabla' }
        #requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        while True:
            paragraphs, self.newest_email_date = getEmails(self.sender, self.subject)
            if self.newest_email_date != self.last_email_date:
                print("request begin")
                requests.post(self.webhook_url, data=paragraphs[1].getText(), headers={'Content-Type': 'application/json'})
                print("request over")
                self.order_info = json.loads(paragraphs[1].getText())
                print("Date: ", self.newest_email_date)
                print("Alert:")
                print(self.order_info)
                self.last_email_date = self.newest_email_date
        
if __name__ == '__main__':
    
    handler = Handler()
    t_list = []
    t_list.append(Thread(target=handler.get_emails))
    for t in t_list:
        t.start()
    for t in t_list:
        t.join()
