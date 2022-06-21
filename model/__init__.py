from app import app
from flask import request, session, jsonify
from helpers.database import *
from helpers.hashpass import *
#from helpers.mailer import *
from bson import json_util, ObjectId
import json
UserId = 'zrJHkJucQ9OXTBoP7oQg0A4Fx4b2'
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

def stack_dicts_elements(d_stack,d_new,keys_excluded=None):
    keys = list(d_new.keys())
    if keys_excluded is not None:
        for k in keys_excluded:            
            keys.remove(k)
            
    for key in keys:  
        if type(d_new[key]) is dict:
            if key not in d_stack:
                d_stack[key] = {}
                
            d_stack[key] = stack_dicts_elements(d_stack[key],d_new[key])
        else:
            if key not in d_stack:
                d_stack[key] = []
            d_stack[key].append(d_new[key])
    return d_stack
def getSessions():
    sessions = db.collection('users').document(UserId).collection('more_user_info').document('SessionsDoc')\
    .collection('Sessions').stream()
    final_sessions = []
    for session in sessions:
        final_sessions.append(session.to_dict())
    result = {}
    for session in final_sessions:
        timestamp = session['timestamp']
        if timestamp not in result:
            result[timestamp] = {}
        result[timestamp] = stack_dicts_elements(result[timestamp],session,['timestamp'])  
    return result
def getLevels():
    levels = db.collection('users').document(UserId).collection('more_user_info').document('levels_stats').get().to_dict()
    return levels