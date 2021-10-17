import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../"))

from pycs.LocalWorldModel import LocalWorldModel
from pycs.ConstructionSet import ConstructionSetApp
from pycs.ImageCollection import ImageCollection

if __name__ == "__main__":
    json_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./test_data/test_data.json")

    with LocalWorldModel(json_file) as wm:
        ic = ImageCollection()
        cs = ConstructionSetApp(wm, ic)
        cs.start()
