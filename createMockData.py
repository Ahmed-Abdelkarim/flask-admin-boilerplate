import random
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore 
import json
cred = credentials.Certificate("./key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

playerStats = db.collection('playerStats').stream()

sessionTimes = []
for p  in playerStats:
    sessionTimes.append(p.to_dict()['lastSessionTime'])

with open("output.json", "w") as f:
    json.dump(sessionTimes, f)