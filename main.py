from os import path
import os
from utility.tar_utility import TarReader
from utility.mongo_utility import MongoHelper
from ILSVRC2012.xml_parser import BBoxXmlHandle
import xml.sax
import argparse
from queue import  Empty
from multiprocessing import Queue
import multiprocessing

bboxPath = path.expanduser('~') + '/data/dataset/ImageNet/ILSVRC2012_bbox_train_v2.tar'


def parserImageNetBBox():
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


def parserImageNetStorage(queue,root):
    print('subprocess start pid={}'.format(os.getppid()))
    while True:
        try:
            d = queue.get(timeout=1)
        except Empty as e:
            print(e)
            continue
        # finally:
        #     print('error!!! subprocess exit pid  ={}'.format(os.getppid()))
        d = queue.get()
        if not d:
            print('timeout')
            continue
        if d == 'exit':
            print('exit pid={}',os.getppid(),end='|')
            queue.put(d)
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()  # 创建ArgumentParser()对象
    parser.add_argument('--train')  # 调用 add_argument() 方法添加参数
    parser.add_argument('--bbox', type=bool,default=False)
    args = parser.parse_args()  # 使用 parse_args()解析出参数
    if args.bbox:
        pass
    print(args.train)
    q = Queue()
    # tars = [args.train + tar for tar in os.walk(args.train)]
    tasks = [multiprocessing.Process(target=parserImageNetStorage, args=(q, args.train)) for _ in range(2)]
    for task in tasks:
        task.start()

    for tar in os.walk(args.train):
        q.put(tar)
        print(tar)
    q.put('exit')
    for task in tasks:
        task.join()
    print('finish')
    # print(tars)