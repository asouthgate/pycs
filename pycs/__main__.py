import argparse as ap

from pycs.WorldModel import WorldModel
from pycs.ConstructionSet import ConstructionSetApp

if __name__ == "__main__":
    wm = WorldModel(json_fpath)
    cs = ConstructonSetApp(wm)
    cs.main()
