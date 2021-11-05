import sys
import os
import unittest

from unittest.mock import Mock
from unittest.mock import patch

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../"))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_data2/"))

from pycs.LocalWorldModel import LocalWorldModel
from pycs.ConstructionSet import ConstructionSetApp
from pycs.FileSystemDataLoader import FileSystemDataLoader

class TestConstructionSetClicking(unittest.TestCase):

    def setUp(self):
        self.fsdl = FileSystemDataLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_data2/"))
        self.wm = LocalWorldModel(self.fsdl)
        self.cs = ConstructionSetApp(self.wm)

    def test_click_position(self):

        self.result = None
        def se(x):
            self.cs._click_m1_old(x)
            ret = self.cs._get_canvas_cursor_coords()
            self.cs.exit()
            self.result = ret

        mock = Mock(side_effect = se)
        ConstructionSetApp._click_m1_old = ConstructionSetApp._click_m1
        ConstructionSetApp._click_m1 = mock
        # Have to rebind because Tkinter does something strange here which breaks mocking
        self.cs.canvas.bind('<Button-1>', self.cs._click_m1)
        self.cs.start()

        x, y = self.result
        print(x, y)
        ca = mock.call_args[0][0]
        self.assertLess(x, 50)
        self.assertLess(y, 50)
            
        
