from fastapi import Header, HTTPException, status
from appwrite.client import Client
from appwrite.services.account import Account
from appwrite.services.users import Users
from appwrite.services.messaging import Messaging
from appwrite.services.databases import Databases
from appwrite.id import ID
import json
import os
from dotenv import load_dotenv

load_dotenv()

class AppwriteClient:
    def __init__(self, is_admin=True, jwt=None):
        self.client = self.get_client(is_admin, jwt)
        self.account = Account(self.client)
        self.messaging = Messaging(self.client)
        self.users = Users(self.client)
        self.databases = Databases(self.client)
        self.id = ID()

    @staticmethod
    def get_client(admin=True, jwt=None):
        if admin:
            client = Client()
            client.set_endpoint("https://cloud.appwrite.io/v1")
            client.set_project(os.getenv("APPWRITE_PROJECT"))
            client.set_key(os.getenv("APPWRITE_KEY"))
        else:
            client = Client()
            client.set_endpoint("https://cloud.appwrite.io/v1")
            client.set_project(os.getenv("APPWRITE_PROJECT"))
            client.set_jwt(jwt)
        
        return client


