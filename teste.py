from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
import urllib
import urllib.parse

def teste_connect():
    try:
        load_dotenv()

        mongo_user = os.getenv("MONGO_USER")
        mongo_pass = os.getenv("MONGO_PASS")

        username = urllib.parse.quote_plus(mongo_user)
        password = urllib.parse.quote_plus(mongo_pass)
        client = MongoClient("mongodb+srv://%s:%s@cluster0.gjkin5a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" % (username, password))

        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")

    except Exception as e:
        print(e)

teste_connect()
