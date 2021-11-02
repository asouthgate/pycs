import sys
import os
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("cs." + __name__)

from tkinter import PhotoImage
from PIL import Image, ImageTk

from pycs.interfaces.ImageCollectionABC import ImageCollectionABC
from pycs.ImageSelector import ImageSelector

class CanvasImageCollection(ImageCollectionABC):

    def __init__(self, canvas, x0, y0):
        self.x = x0
        self.y = y0
        self.canvas = canvas
        self.highlight = self.canvas.create_rectangle(0, 0, 0, 0, outline='red', width=10)
        self.photo_images = {}
        self.pi2ci = {}
        self.image_selector = ImageSelector()

        self._new_index = 0

    @property
    def focused_image(self):
        return self.image_selector.focused_image

    def pan(self):
        pass

    def zoom(self):
        pass

    def get_selection_origin(self):
        return self.image_selector.origin_x, self.image_selector.origin_y

    def lift_focused_image(self):
        self.canvas.lift(self.highlight)
        self.canvas.lift(self.pi2ci[self.image_selector.focused_image])

    def lower_focused_image(self):
        self.canvas.lower(self.pi2ci[self.image_selector.focused_image])
        self.canvas.lower(self.highlight)
        
    def get_image_dimensions(self, i):
        return self.photo_images[i].width(), self.photo_images[i].height()

    def get_selected(self):
        return self.image_selector.focused_image

    def delete(self, i):
        del self.photo_images[i]
        self.canvas.delete(self.pi2ci[i])
        del self.pi2ci[i]

    def move_selected_image(self, pointer_x, pointer_y):
        """ Move a selected image based on a difference. """
        photo_image_ind = self.image_selector.focused_image
        photo_image = self.photo_images[photo_image_ind]
        logger.debug("focused image is %s" % photo_image)
#        assert photo_image_ind < len(self.photo_images), "Photo image index greater than number of photo images - 1"
        canvas_image = self.pi2ci[photo_image_ind]

        # Calculate the difference since the origin
        dx = - (self.image_selector.origin_x - pointer_x)
        dy = - (self.image_selector.origin_y - pointer_y)

        # Set a new origin
        self.image_selector.origin_x = pointer_x
        self.image_selector.origin_y = pointer_y

        x, y = self.canvas.coords(canvas_image)

        new_x = x + dx
        new_y = y + dy

        # Move the selected image
        self.canvas.moveto(canvas_image, new_x, new_y)
        
        # Move the highlight
        self.move_highlight_to_selected_image()

        return new_x, new_y

    def click(self, x, y):
        self.image_selector.click(x, y)

    def select_image(self, nearest):
#        assert nearest < len(self.photo_images), "Photo image index %d greater than number of photo images %d - 1" % (nearest, len(self.photo_images))
        self.image_selector.select_image(nearest)
        self.move_highlight_to_selected_image()

    def release(self):
        self.image_selector.release()

    def select_next_image(self, cnear, x, y):
        # TODO: what is cnear
        self.image_selector.select_next_image(cnear, x, y)
        self.move_highlight_to_selected_image()

    def select_prev_image(self, cnear, x, y):
        self.image_selector.select_prev_image(cnear, x, y)
        self.move_highlight_to_selected_image()

    def move_image(self, j):
        """ Move an image. """
        pass

    def get_new_index(self):
        ni = self._new_index
        self._new_index += 1
        return ni

    def add_image(self, png, x, y, w=None, h=None, anchor="nw"):
        logger.debug("opening image %s" % (png))
        tmpimage = Image.open(png)
        if w and h:
            tmpimage = tmpimage.resize((w, h))
        tmppi = ImageTk.PhotoImage(tmpimage)
        new_ind = self.get_new_index()
        self.photo_images[new_ind] = tmppi
        logger.debug("creating image %s from %s" % (tmppi, png))
        ci = self.canvas.create_image(x, y, image=tmppi, anchor="nw")
        self.pi2ci[new_ind] = ci
        return new_ind

    def move_highlight(self, x1, y1, x2, y2):
        self.canvas.coords(self.highlight, x1, y1, x2, y2)

    def move_highlight_to_selected_image(self):
        photo_image_n = self.image_selector.focused_image
#        assert photo_image_n < len(self.photo_images)
        # rename function if it selects and highlights
        coords = self.canvas.coords(self.pi2ci[photo_image_n])
        print("moving highlight to image", photo_image_n, "at",  coords)
        x, y = coords
        # TODO: take args for new new width and height, or new bottom right
        self.move_highlight(x, y,
                           x + self.photo_images[photo_image_n].width(),
                           y + self.photo_images[photo_image_n].height())
        self.canvas.tag_lower(self.highlight, self.pi2ci[photo_image_n])


