from app import app
from flask import request, session, jsonify
from helpers.database import *
from helpers.hashpass import *
#from helpers.mailer import *
from bson import json_util, ObjectId
import json

def checkloginusername():
    username = request.form["username"]
    doc_ref = db.collection('users').document(f'{username}')
    check = doc_ref.get().exists
    if check is None:
        return "No User"
    else:
        return "User exists"

def checkloginpassword():
    username = request.form["username"]
    doc_ref = db.collection('users').document(f'{username}')
    check = doc_ref.get().to_dict()
    password = request.form["password"]
    hashpassword = getHashed(password)
    if hashpassword == check["password"]:
        #endmail(subject="Login on Flask Admin Boilerplate", sender="Flask Admin Boilerplate", recipient=check["email"], body="You successfully logged in on Flask Admin Boilerplate")
        session["username"] = username
        return "correct"
    else:
        return "wrong"
    

def checkusername():
    username = request.form["username"]
    doc_ref = db.collection('users').document(f'{username}')
    check = doc_ref.get().exists
    if check is None:
        return "Available"
    else:
        return "Username taken"

def registerUser():
    fields = [k for k in request.form]                                      
    values = [request.form[k] for k in request.form]
    data = dict(zip(fields, values))
    user_data = json.loads(json_util.dumps(data))
    user_data["password"] = getHashed(user_data["password"])
    user_data["confirmpassword"] = getHashed(user_data["confirmpassword"])
    username = user_data['username']
    db.collection('users').document(f'{username}').set(user_data)
    #sendmail(subject="Registration for Flask Admin Boilerplate", sender="Flask Admin Boilerplate", recipient=user_data["email"], body="You successfully registered on Flask Admin Boilerplate")
    print("Done")

def getPlayerStats():
    playerStats = db.collection('playerStats').stream()
    sessionTimes = []
    for p in playerStats:
        sessionTimes.append(p.to_dict()['lastSessionTime'])
    return jsonify(sessionTimes)




