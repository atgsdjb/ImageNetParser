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
from tensorflow.image import decode_jpeg
import tensorflow as tf
import sys
import datetime
import gc

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
bboxPath = path.expanduser('~') + '/data/dataset/ImageNet/ILSVRC2012_bbox_train_v2.tar'


def parserImageNetBBox():
    tar = TarReader(bboxPath)
    dbHelper = MongoHelper('ImageNet', 'train_bbox', '')
    i = 0
    for (p, n, d) in tar:
        xmlHandler = BBoxXmlHandle()
        xml.sax.parseString(d,xmlHandler)
        data = xmlHandler.get_data()
        dbHelper.insert(**data)
        print('[{}]'.format(i),end='')
        i = i + 1


def decodeJpeg(image):
    with tf.Session() as session:
        bmp = session.run(decode_jpeg(image))
    return bmp.shape[0],bmp.shape[1],bmp.shape[2], bmp.tobytes()


def parserImageNetStorage(tar,root):
    gc.disable()
    print('subprocess start pid={}'.format(os.getpid()))
    dbHelper = MongoHelper('ImageNet', 'train', '')
    dbTotul = MongoHelper('ImageNet',"complete", '')
    while True:
        tar = TarReader(tar)
        i = 0
        clazz = os.path.basename(tar)[:-4]
        if dbTotul.hashone(clazz=clazz):
            continue

        starttime = datetime.datetime.now()

        for (_, n, tar) in tar:
            i = i + 1
            height, width, depth, data = decodeJpeg(tar)
            try:
                dbHelper.insert(height=height,width=width,depth=depth,name=n,clazz=clazz,data=data)
                print('.', end='')
                pass
            except :
                dbHelper.insert(height=height,width=width,depth=depth,name=n,clazz=clazz,toolarge=True)
                print('#',end='')
                pass
            sys.stdout.flush()
        gc.collect()
        dbTotul.insert(clazz=clazz,count=i)
        print()

        endtime = datetime.datetime.now() - starttime
        print('finish clazz={} duration={}'.format(clazz,endtime.seconds))
        gc.enable()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()  # 创建ArgumentParser()对象
    parser.add_argument('--train')  # 调用 add_argument() 方法添加参数
    parser.add_argument('--bbox', type=bool,default=False)
    args = parser.parse_args()  # 使用 parse_args()解析出参数
    if args.bbox:
        parserImageNetBBox()
        exit(0)
    print(args.train)
    q = Queue()
    tasks = [multiprocessing.Process(target=parserImageNetStorage, args=(q, args.train)) for _ in range(4)]
    for task in tasks:
        task.start()

    for dir,subdir,files in os.walk(args.train):
        for t in files:
            q.put(os.path.join(dir,t))
            print('.',end='|')
        # print(tar)
    print('queue is empyt={}'.format(q.empty()))
    q.put('exit')
    q.put('exit')
    for task in tasks:
        task.join()
    print('finish')
    # print(tars)