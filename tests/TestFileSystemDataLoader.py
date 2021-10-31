import unittest
import os
import sys
import logging
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("test." + __name__)

sys.path.append(os.path.join(os.path.realpath(__file__), ".."))
sys.path.append(os.path.join(os.path.realpath(__file__), "test_data/"))

from pycs.FileSystemDataLoader import FileSystemDataLoader
from pycs.LocalWorldModel import LocalWorldModel

def worldobj_equal(a, b):
    eq_c = 0
    for k, v in a.__dict__.items():
        if a[k] == b[v]:
            eq_c += 1
    if eq_c == len(a.__dict__): 
        return True
    else:
        return False    

class TestFileSystemDataLoader(unittest.TestCase):

    def setUp(self):
        self.fsdl = FileSystemDataLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_data/"))

    def tearDown(self): pass

    def test_read(self):
        logger.debug("\nTesting read!")
        with self.fsdl as dl:
            [logger.debug(dr) for dr in dl]
        with self.fsdl as dl:
            drs = [dr for dr in dl]
            logger.debug("drs: %s" % str(drs))
            self.assertTrue(drs)

    def test_write(self):
        outfn = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_data/test_write_dir/")

        # Write
        with self.fsdl as fsdl1:
            self.fsdl.write([dr for dr in fsdl1], root_folder_name=outfn)

        # Test that it is loadable json at all        
        with open(os.path.join(outfn, "data.json")) as jsonf:
            loaded = json.load(jsonf)
            print(loaded)

        # Test that it is correct
        with FileSystemDataLoader(outfn) as fsdl2, self.fsdl as fsdl1:
            drs2 = [dr for dr in fsdl2]
            drs1 = [dr for dr in fsdl1]
            for i, dr in enumerate(drs1):
                self.assertEqual(drs2[i], dr)

    def test_write_and_load_integration(self):
        wm = LocalWorldModel(self.fsdl)
        objects = [wo.data_dict for wo in wm]
        outfn = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_data/test_write_dir/")
        self.fsdl.write(objects, root_folder_name=outfn)
        with FileSystemDataLoader(outfn) as fsdl2:
            for data_resource in fsdl2:
                pass

            
