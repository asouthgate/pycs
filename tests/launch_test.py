import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../"))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_data/"))


from pycs.LocalWorldModel import LocalWorldModel
from pycs.ConstructionSet import ConstructionSetApp
from pycs.FileSystemDataLoader import FileSystemDataLoader

if __name__ == "__main__":

    fsdl = FileSystemDataLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_data/"))

    wm = LocalWorldModel(fsdl)
    cs = ConstructionSetApp(wm)
    cs.start()
