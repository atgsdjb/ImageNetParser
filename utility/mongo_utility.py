import pymongo

class SchemError(BaseException):
    pass


class MongoHelper:
    def __init__(self,database,collection,schem,username=None,password=None):
        self.client = pymongo.MongoClient()
        self.schem = schem
        self.collection = self.client[database][collection]
        print(self.collection)

    def _check_(self,keys):
        pass
        return True

    def insert(self,**dict):
        if not self._check_(dict):
            raise SchemError()
        self.collection.insert(dict)
        return

    def hashone(self,**dict):
            return self.collection.count(dict) != 0

    def insert_xml(self,xml):
        pass

    def insert_json(self,json):
        return

    def __del__(self):
        self.client.close()
        return