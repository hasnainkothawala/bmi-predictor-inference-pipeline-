import os
from pymongo import MongoClient
from datetime import date


class Base_DAO:
    def __init__(self):
        self.MONGO_HOST = os.getenv("MONGO_HOST")
        # self.MONGO_PORT = int(os.getenv("MONGO_PORT"))
        self.MONGO_USER = os.getenv("MONGO_USER")
        self.MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
        self.AUTH_DATABASE = os.getenv("AUTH_DATABASE")
        self.PRED_DATABASE = os.getenv("DATABASE_NAME")
        self.PRED_COLLECTION = os.getenv("COLLECTION_NAME")
        print(f"Mongo Host: {self.MONGO_HOST}")
        self.mongo_client = MongoClient(
            self.MONGO_HOST,
            # username=self.MONGO_USER,
            # password=self.MONGO_PASSWORD,
            authSource=self.AUTH_DATABASE,
            # authMechanism="SCRAM-SHA-256",
            connect=True,
            retryWrites=False,
        )

        self.connection_pool = {}

    def insert_preds_to_db(self, data):
        db = self.mongo_client[self.PRED_DATABASE]
        collection = db[self.PRED_COLLECTION]
        collection.insert_one(data)


class BMI_DAO:
    def __init__(self, app_id: int, age: int, gender: str, height: int, weight: int, bmi: float,
                 issue_date: date = date.today().strftime("%b-%d-%Y")):
        self.app_id = app_id
        self.age = age
        self.gender = gender
        self.height = height
        self.weight = weight
        self.issue_date = issue_date
        self.bmi = bmi
