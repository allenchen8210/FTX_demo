import os
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