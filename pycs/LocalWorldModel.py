import json
import random
import math
import traceback
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("cs." + __name__)

from PIL import ImageTk
from pycs.interfaces.WorldModelABC import WorldModelABC
from pycs.interfaces.WorldModelABC import WorldObjectABC

from pycs.interfaces.DataLoaderABC import DataLoaderABC

class WorldObject(WorldObjectABC):
    """
    An entity; used to define data associated with any object in the world model.

    Attributes:
        name:
        png:
        v:

    Optional args:
        w:
        h:
    """

    def __init__(self, name, png, x, y, w=0, h=0):
        self._name = str(name)
        self._png = png
        self._v = [x, y]
        self._w = w
        self._h = h        
        self.initialized = True

    @property
    def data_dict(self):
        return { "v": self._v, "w": self._w, "h": self._h, 
                 "filename": self._png.split("/")[-1],
                 "name": self._name }

    @property
    def x(self):
        return self._v[0]
    
    @x.setter
    def x(self, u):
        self._v[0] = u

    @property
    def y(self):
        return self._v[1]
        
    @y.setter
    def y(self, u):
        self._v[1] = u

    @property
    def w(self):
        return self._w

    @property
    def h(self):
        return self._h

    @property
    def png(self):
        return self._png

    @property
    def name(self):
        return self._name

class LocalWorldModel(WorldModelABC):
    """
    A model of the world in local memory, stored in json.

    Attributes:
        world_objects:
    """

    def __init__(self, data_loader):

        self.world_objects = []
        self.data_loader = data_loader

        with data_loader as dl:
            for obj in dl:
                logger.debug("creating object %s with data x=%d y=%d w=%d h=%d" % (obj['name'], *obj['v'], obj['w'], obj['h']))
                wo = WorldObject(obj['name'], obj['filename'], *obj['v'], obj['w'], obj['h'])
                self.world_objects.append(wo)

#    def __enter__(self):
#        return self

#    def __exit__(self, type, value, tb):
#        if tb:
#            print("".join(traceback.format_tb(tb)), type, value)
#        return self

    def __iter__(self):
        for ent in self.world_objects:
            yield ent

    def __getitem__(self, x):
        pass
   
    def __setitem__(self, x, v):
        pass

    def _index(self):
        # fast spatial index for retrieving objects
        pass

    def save(self, fname=None):
        logger.debug("saving world model!")
        self.data_loader.write([wo.data_dict for wo in self.world_objects], root_folder_name=fname)
    
    def update_object_x(self, i, new_x):
        self.world_objects[i].x = new_x
    
    def update_object_y(self, i, new_y):
        self.world_objects[i].y = new_y

    def add_world_object(self, wo):
        self.world_objects.append(wo)

    def duplicate_world_object(self, i, x, y):
        wo = self.world_objects[i]
        name = wo.name + "_copy"
        png = wo.png
        w = wo.w
        h = wo.h
        return self.new_world_object(name, png, x, y, w=w, h=h)

    def new_world_object(self, name, png_filename, x, y, w=None, h=None):
        wo = WorldObject(name, png_filename, x, y, w=w, h=h)
        self.add_world_object(wo)
        return wo
        
    def query(self, v_ul, v_br):
        # query for objects in box between v_ul and v_br
        pass

    def find_near(self, x, y, r=300):
        logging.debug("querying near %d %d %d" % (x, y, r))
        res = []
        for wi, wo in enumerate(self.world_objects):
            # taxicab
            dr = math.fabs(wo.x - x) + math.fabs(wo.y - y)
            if dr < r:
                res.append((wi, dr))
        return [t[0] for t in sorted(res, key=lambda x:x[1])]

    def find_nearest(self, x, y):
        logging.debug("querying nearest %d %d" % (x, y))
        res = []
        for wi, wo in enumerate(self.world_objects):
            # taxicab
            dr = math.fabs(wo.x + ( wo.w / 2 ) - x) + math.fabs(wo.y + ( wo.h / 2) - y)
            res.append((wi, wo.x, wo.y, dr))
        mini = min(res, key=lambda x:x[3])
        logging.debug("found %d nearest!" % mini[0])
        return mini[0]


