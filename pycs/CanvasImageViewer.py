from pycs.ImageViewerABC.interfaces import ImageViewerABC

class CanvasImageViewer(ImageViewerABC):

    def __init__(self, x0, y0, images):
        self.x = x0
        self.y = y0
        self.images = images

    def pan(self):
        pass

    def zoom(self):
        pass

    def move_image(self, j):
        """ Move an image. """
        pass
