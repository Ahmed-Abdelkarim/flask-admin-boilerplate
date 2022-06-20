# from pymongo import MongoClient
# import configuration

# connection_params = configuration.connection_params

# #connect to mongodb
# mongoconnection = MongoClient(
#     'mongodb://{user}:{password}@{host}:'
#     '{port}/{namespace}?retryWrites=false'.format(**connection_params)
# )

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore 
cred = credentials.Certificate("./key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# db = mongoconnection.databasename
