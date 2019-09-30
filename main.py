import os
from utility.tar_utility import TarReader
from utility.mongo_utility import  MongoHelper
from ILSVRC2012.xml_parser import  BBoxXmlHandle
import xml.sax


def imageNettoMongo(self,file=''):
    tar = TarReader(file)
    for (xml, _, _) in tar:
        print(xml)


if __name__ == '__main__':
    print('main')
    handler = BBoxXmlHandle()
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    # 重写 ContextHandler
    parser.setContentHandler(handler)
    parser.parse("/Users/seraph/Downloads/n01440764/n01440764_8240.xml")
    print('result{}| name ={}'.format(handler, handler.name))
    h = MongoHelper('test','test',['name','old'])
    h.insert(name='seraph',old=12)
