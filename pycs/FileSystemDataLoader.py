import os
import json
import traceback
from pycs.interfaces.DataLoaderABC import DataLoaderABC

class DataResource:
    def __init__(self, d, ):
        self.v = d['v']
        self.w = d['w']
        self.h = d['h']
        self.filename = d['filename']
        self.name = d['name']
 
class FileSystemDataLoader(DataLoaderABC):

    def __init__(self, root_path):
        self.root_path = root_path
        self.json_fpath = os.path.join(root_path, "data.json")
        print(self.json_fpath)
        self.json_file = None

    def __enter__(self):
        self.json_file = open(self.json_fpath)
        return self

    def __exit__(self, type, value, tb):
        self.json_file.close()        
        if tb:
            print("".join(traceback.format_tb(tb)), type, value)
        return self

    def __iter__(self):
        print("???")
        objects = [obj for obj in json.load(self.json_file)['objects']]
        print(objects)
        print("wtf")
        for obj in objects:
            obj['filename'] = os.path.join(self.root_path, obj['filename'])
            dr = DataResource(obj)
            print(dr.__dict__)
            yield dr 
    def get(self, fname):
        return os.path.join(self.root_path, fname)


