#!/usr/bin/env python3
import hashlib

from pymongo import MongoClient


class Authenticator:
    def __init__(self):
        client = MongoClient()
        db = client["ECE4564_Assignment_3"]
        self.collection = db["service_auth"]
        self.collection.insert_one({
            "username": 'khaled',
            "password": hashlib.sha256('khaled'.encode('utf-8')).hexdigest()
        })
        self.collection.insert_one({
            "username": 'enzo',
            "password": hashlib.sha256('enzo'.encode('utf-8')).hexdigest()
        })
        self.collection.insert_one({
            "username": 'joseph',
            "password": hashlib.sha256('joseph'.encode('utf-8')).hexdigest()
        })

    def insert_record(self, username: str, password: str) -> None:
        self.collection.insert_one({
            "username": username,
            "password": hashlib.sha256(password.encode('utf-8')).hexdigest()
        })
        return True

    def authenticate_record(self, username: str, password: str) -> bool:
        record = self.collection.find_one({"username": username})
        if not record:
            return False
        db_uname = record.get("username", None)
        print(username)
        print(db_uname)
        db_pass = record.get("password", None)
        print(password)
        print(db_pass)

        if db_uname and db_pass and username == db_uname and hashlib.sha256(password.encode('utf-8')).hexdigest() == db_pass:
            return True
        return False
