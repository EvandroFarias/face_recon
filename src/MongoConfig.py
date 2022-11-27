from cgi import test
from pymongo import MongoClient

class MongoConnectionClient:
    _db = None

    def __init__(self, host: str, port: int):
        self._db = MongoClient(host, port)
        self._collection = None

    def connect_to_collection(self, dbname: str, collection_name: str):
        database = self._db[dbname]
        collection = database[collection_name]
        self._collection = collection

    def select_all(self):
        lista_do_select = []
        for i in self._collection.find():
            lista_do_select.append(i)
        return lista_do_select

    def insert_one(self, args):
        self._collection.insert_one(args)