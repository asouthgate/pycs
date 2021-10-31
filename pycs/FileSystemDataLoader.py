import os
import json
import traceback
from pycs.interfaces.DataLoaderABC import DataLoaderABC
from pycs.interfaces.WorldModelABC import WorldObjectABC

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# YAGNI?
#class DataResource:
#    """ Class used to hold data from json; a game entity. """
#    def __init__(self, d):
#        self.v = d['v']
#        self.w = d['w']
#        self.h = d['h']
#        self.filename = d['filename']
#        self.name = d['name']
    
# YAGNI?
#class DataResourceJSONEncoder(json.JSONEncoder):
#    """ Encoder for turning data resources into JSON. """
#    def default(self, obj):
#        return obj.__dict__
 
class FileSystemDataLoader(DataLoaderABC):
    """ Used to load data from a filesystem with a particular structure. """

    def __init__(self, root_path):
        self.root_path = root_path
        if not os.path.isdir(root_path):
            raise Exception("%s is not an extant folder." % root_path)
        self.json_fpath = os.path.join(root_path, "data.json")
        self.json_file = None
        self.json_obj = None
        self.open = False

    def __enter__(self):
        if self.open:
            raise Exception("Tried to open twice! Close first!")           

        self.json_file = open(self.json_fpath)
        self.open = True
        return self

    def __exit__(self, type, value, tb):
        self.json_file.close()        
        if tb:
            print("".join(traceback.format_tb(tb)), type, value)
        self.open= False
        return self

    def __iter__(self):
        """ Iterate through data objects. """
        loaded_json = json.load(self.json_file)
        logger.debug(loaded_json)
        objects = [obj for obj in loaded_json['objects']] 
        for obj in objects:
            obj['filename'] = os.path.join(self.root_path, obj['filename'])
#            dr = DataResource(obj)
            yield obj

#    def get_abs_path(self, fname):
#        return os.path.join(self.root_path, fname)

    def get(self): pass

    def write(self, encodeables, root_folder_name=None):
        """ Write encodeable objects to JSON. """
        if not os.path.isdir(root_folder_name):
            raise Exception("%s is not an extant folder." % root_path)
        fname = os.path.join(root_folder_name, "data.json") if root_folder_name else self.json_fpath
        with open(fname , "w") as of:
#            json.dump(encodeables, of, cls=DataResourceJSONEncoder)
            json.dump({"objects":encodeables}, of)
            


