from utility.tar_utility import TarReader
from utility.mongo_utility import  MongoHelper
from ILSVRC2012.xml_parser import  BBoxXmlHandle
import xml.sax


def imageNettoMongo(self,file=''):
    tar = TarReader(file)
    for (p, n, d) in tar:
        print(p)


if __name__ == '__main__':
    print('main')
    handler = BBoxXmlHandle()
