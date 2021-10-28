import unittest
import sys
import os
import tkinter
import json

sys.path.append(os.path.join(os.path.realpath(__file__), ".."))

from pycs.CanvasImageViewer import CanvasImageViewer
from pycs.FileSystemDataLoader import FileSystemDataLoader

class CanvasImagerViewerTester(unittest.TestCase):

    def setUp(self):
        self.root = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.root, width=500, height=500)
        self.civ = CanvasImageViewer(self.canvas, 0, 0)
        # get some data
        data_loader = FileSystemDataLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_data/"))
        with data_loader as dl:
            for obj in dl:
                sys.stderr.write("adding an image %s\n" % obj.filename)
                self.civ.add_image(*obj.v, obj.w, obj.h, obj.filename)

    def tearDown(self):
        self.root.destroy()

    def test_select_image(self):  
        # Setup 
#        self.setup()
        for k in range(len(self.civ.photo_images)):
            # Exercise: select an image
            self.civ.select_image(k)

            # Verify
            self.assertEqual(self.civ.focused_image, k)

    def test_move_highlight_to_selected_image(self):
        # Setup 
        # implicit
        for k in range(len(self.civ.photo_images)):
            ck = self.civ.pi2ci[k]
            # Exercise

            self.civ.select_image(k)        
            
            # Exercise: move highlight

            self.civ.move_highlight_to_selected_image()

            # Verify
            hl_coords = self.canvas.coords(self.civ.highlight)
            hl_x1, hl_y1, hl_x2, hl_y2 = hl_coords
            im_k_coords = self.canvas.coords(ck)
            im_x1, im_y1 = im_k_coords
            im_w = self.civ.photo_images[k].width() 
            im_h = self.civ.photo_images[k].height() 

            self.assertEqual(hl_x1, im_x1)
            self.assertEqual(hl_y1, im_y1)
            self.assertEqual(hl_x2, im_x1+im_w)
            self.assertEqual(hl_y2, im_y1+im_h)


    def test_move_selected_image(self):
        pass
