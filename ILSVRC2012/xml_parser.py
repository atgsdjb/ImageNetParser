import xml.sax
import queue


class BBoxXmlHandle(xml.sax.ContentHandler):

    def __init__(self):
        self.name = ''
        self.path = ''
        self.width = -1
        self.height = -1
        self.depth = -1
        self.objects=[]
        self.currentTag = ''
        self.currentObj = None
        self.contents = []

    def startElement(self, tag, attributes):
        self.currentTag = tag
        self.contents.append('')
        if tag == 'object':
            self.currentObj = {}

    def characters(self, content):
        self.contents[-1] = self.contents[-1] + content

    def endElement(self,tag):
        content = self.contents.pop().strip()
        if tag == 'filename':
            self.name = content
        elif tag == 'folder':
            self.path = content
        elif tag == 'width':
            self.width = int(content)
        elif tag == 'height':
            self.height = int(content)
        elif tag == 'depth':
            self.depth = int(content)
        elif tag == 'xmin':
            self.currentObj['xmin'] = int(content)
        elif tag == 'ymin':
            self.currentObj['ymin'] = int(content)
        elif tag == 'xmax':
            self.currentObj['xmax'] = int(content)
        elif tag == 'ymax':
            self.currentObj['ymax'] = int(content)
        elif tag == 'object':
            self.objects.append(self.currentObj)

    def get_data(self):
        return {'name':self.name,'path':self.path,'width':self.width,'height':self.height,
                'depth':self.depth,'bbox':self.objects}

    def __str__(self):
        return 'name=[{}],height=[{}] objects=[{}]'.format(self.name,self.height,self.objects)
