from os import path
from utility.tar_utility import TarReader
from utility.mongo_utility import  MongoHelper
from ILSVRC2012.xml_parser import  BBoxXmlHandle
import xml.sax

bboxPath = path.expanduser('~') + '/data/dataset/ImageNet/ILSVRC2012_bbox_train_v2.tar'


def imageNetStorage(root='.'):
    tar = TarReader(bboxPath)
    dbHelper = MongoHelper('ImageNet','train','')
    i = 0
    for (p, n, d) in tar:
        xmlHandler = BBoxXmlHandle()
        xml.sax.parseString(d,xmlHandler)
        data = xmlHandler.get_data()
        dbHelper.insert(**data)
        print('[{}]'.format(i),end='')
        i = i + 1


if __name__ == '__main__':
    print(bboxPath)
    imageNetStorage()
