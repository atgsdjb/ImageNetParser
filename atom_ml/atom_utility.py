import csv
import numpy as np
import sys
def loadCsv(fn):
    reader = csv.reader(fn)
    data = []
    for row in reader:
            r = []
    return [i for i in reader]

class PackPLA():
    pass


class PLA():
    def __init__(self,shape):
        pass
        # self.weight = np.random.normal(0,0.1,size=(shape[1]+1,))
        self.weight = np.zeros(shape=(shape[1]+1,))

    def train(self, X, Y, lr=1,epoch=1):
        o = 0
        e = 0
        train_x = np.ones((X.shape[0],X.shape[1]+1))
        train_x[:,1:] = X
        for _ in range(epoch):
            np.random.shuffle(train_x)
            for x,y in zip(train_x,Y):
                yh = np.dot(x,self.weight) * y
                if yh <= 0 :
                    e += 1
                    weight = self.weight + x * y * lr
                    self.costAndUpdate(weight, train_x, Y)
                    # print('#',end='#')
                    # sys.stdout.flush()
                else:
                    pass
                    # print('.',end='')
                    # sys.stdout.flush()
        print('o={},e={} weight={}',o,e,self.weight)
        return e

    def costAndUpdate(self,weight,x,y):
        cost0 = np.mean((np.matmul(x,self.weight) * y) <= 0)
        cost1 = np.mean((np.matmul(x,weight) * y) <= 0)
        print('before=[{}=<{}>],after=[{}=<{}>]'.format(cost0,self.weight, cost1,weight))
        if cost0 > cost1 :
            self.weight = weight
        return cost0 , cost1

    def cost(self, X, Y):
        train_x = np.ones((X.shape[0],X.shape[1]+1))
        train_x[:,1:] = X
        return np.mean((np.matmul(train_x,self.weight) * Y) < 0)

    def test(self,x,y):
        pass


if __name__  == '__main__':
    print(__file__)