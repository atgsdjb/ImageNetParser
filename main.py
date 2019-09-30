from os import path
import os
from utility.tar_utility import TarReader
from utility.mongo_utility import MongoHelper
from ILSVRC2012.xml_parser import BBoxXmlHandle
import xml.sax
import argparse
import multiprocessing
from tensorflow.image import decode_jpeg
import tensorflow as tf
import sys
import datetime

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
bboxPath = path.expanduser('~') + '/data/dataset/ImageNet/ILSVRC2012_bbox_train_v2.tar'
total_subprocess = 10

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


def deleteCompleted(tar):
    pass

def decodeJpeg(image):
    with tf.Session() as session:
        bmp = session.run(decode_jpeg(image))
    return bmp.shape[0],bmp.shape[1],bmp.shape[2], bmp.tobytes()


def parserImageNetStorage(tarFile, clazz):
    print('subprocess start pid={}'.format(os.getpid()))
    dbHelper = MongoHelper('ImageNet', 'train', '')
    dbTotul = MongoHelper('ImageNet',"complete", '')
    tar = TarReader(tarFile)
    i = 0
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
    dbTotul.insert(clazz=clazz,count=i)
    print()
    endtime = datetime.datetime.now() - starttime
    #os.remove(tarFile)
    deleteCompleted(tarFile)
    print('finish clazz={} duration={}'.format(clazz,endtime.seconds))
    return 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()  # 创建ArgumentParser()对象
    parser.add_argument('--train')  # 调用 add_argument() 方法添加参数
    parser.add_argument('--bbox', type=bool,default=False)
    args = parser.parse_args()  # 使用 parse_args()解析出参数

    dbTotul = MongoHelper('ImageNet', "complete", '')
    if args.bbox:
        parserImageNetBBox()
        exit(0)
    print(args.train)
    tars = []
    tasks = []
    for dir,subdir,files in os.walk(args.train):
        for t in files:
            tars.append(os.path.join(dir,t))
    print(len(tars))
    for tar in tars:
        print('~',end='')
        sys.stdout.flush()
        clazz = os.path.basename(tar)[:-4]
        if dbTotul.hashone(clazz=clazz):
            print('{} is complete',format(clazz))
            deleteCompleted(tar)
            continue
        if len(tasks) < total_subprocess:
            task = multiprocessing.Process(target=parserImageNetStorage,args=(tar,clazz))
            tasks.append(task)
            task.start()
            continue

#监控子进程是否有完成的
        while len(tasks) == total_subprocess:
            print('$',end='')
            sys.stdout.flush()
            for task in tasks:
                task.join(timeout=10)
                code = task.exitcode
                print('rst {}'.format(code))
                if code is None:
                    continue
                print('task finish rst_code={}'.format(code))
                # task.close()
                tasks.remove(task)
                break
    print('finish')
    # print(tars)
