import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../"))

from pycs.WorldModel import WorldModel
from pycs.ConstructionSet import ConstructionSetApp

if __name__ == "__main__":
    json_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./test_data/test_data.json")
    print(json_file)

    wm = WorldModel(json_file)
    cs = ConstructionSetApp(wm)
    cs.start()
