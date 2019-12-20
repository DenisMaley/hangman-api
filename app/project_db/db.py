from pymongo import MongoClient


class MongoDB(object):
    __db = None

    @classmethod
    def get_connection(cls):
        if cls.__db is None:
            client = MongoClient("mongodb://my_db:27017")
            cls.__db = client.projectDB

        return cls.__db
