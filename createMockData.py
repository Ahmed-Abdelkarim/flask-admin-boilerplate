import random
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore 
import json
cred = credentials.Certificate("./key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

for i in range(20):
    pass
        
    '''
    session_doc = {
        'timestamp': datetime(2022, 6, random.randint(1,5)),
        'time': random.uniform(0,1000),
        'characters': {
            'listening':{
                '0':{
                    'rightanswers':random.randint(0,10),
                    'wronganswers':random.randint(0,10),
                    'numberoftrials':random.randint(0,10)
                },'1':{
                    'rightanswers':random.randint(0,10),
                    'wronganswers':random.randint(0,10),
                    'numberoftrials':random.randint(0,10)
                },'2':{
                    'rightanswers':random.randint(0,10),
                    'wronganswers':random.randint(0,10),
                    'numberoftrials':random.randint(0,10)
                }
            },
            'speaking':{
            '0':{
                    'rightanswers':random.randint(0,10),
                    'wronganswers':random.randint(0,10),
                    'numberoftrials':random.randint(0,10)
                },'1':{
                    'rightanswers':random.randint(0,10),
                    'wronganswers':random.randint(0,10),
                    'numberoftrials':random.randint(0,10)
                },'2':{
                    'rightanswers':random.randint(0,10),
                    'wronganswers':random.randint(0,10),
                    'numberoftrials':random.randint(0,10)
                }
            }
        }
    }
    '''
    ## Add a new doc in collection 'cities' with ID 'LA'
    # db.collection('users').document('zrJHkJucQ9OXTBoP7oQg0A4Fx4b2').collection('more_user_info').document('SessionsDoc')\
    # .collection('Sessions').add(session_doc)
levels_doc = {}
for i in range(3):
    levels_doc["level_"+str(i)] = {
        "Best_Time":random.randint(0,1000)
        ,"Best_Lives":random.randint(0,3)}
    db.collection('users').document('zrJHkJucQ9OXTBoP7oQg0A4Fx4b2').collection('more_user_info').document('levels_stats')\
        .set(levels_doc)