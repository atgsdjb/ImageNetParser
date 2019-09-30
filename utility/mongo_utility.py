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

    def insert_xml(self,xml):
        pass

    def insert_json(self,json):
        pass

    def __del__(self):
        self.client.close()