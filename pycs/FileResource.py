from pycs.interfaces.ResourceABC import ResourceABC

class FileResource(ResourceABC):

    def __init__(self, fpath):

        self.fpath = fpath
        self.fh = None

    def __enter__(self):
        self.fh = open(self.fpath)

    def __exit__(self):
        self.fh.close()
