import os
import tarfile


class TarReader:
    def __init__(self,full_path):
        self.tar = tarfile.open(full_path)

    def __iter__(self):
        return self

    def __next__(self):
        info = self.tar.next()
        while True:
            if info.isdir():
                info = self.tar.next()
                continue
            break
        buf = self.tar.extractfile(info)
        return (os.path.dirname(info.name) , os.path.basename(info.name),buf.read())

    def __del__(self):
        print('close....')
        self.tar.close()
