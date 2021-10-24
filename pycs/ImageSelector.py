import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("cs." + __name__)

class ImageSelector:
    """ 
    Class responsible for selection of objects on a canvas
    """
    def __init__(self):
        self._focused_image = 2
        self.tab_counter = 0
        self.origin_x = None
        self.origin_y = None
        self.picked_up = False

    @property
    def focused_image(self):
        logger.debug("getting focused image %d" % self._focused_image)
        return self._focused_image
    
    @focused_image.setter
    def focused_image(self, x):
        logger.debug("setting focused image to %d" % x)
        self._focused_image = x

    def click(self, x, y):
        self.origin_x = x
        self.origin_y = y
    
    def release(self):
        if self.picked_up:
            print("moving!")
            self.picked_up = False
            self.picker_offset_x = 0
            self.picker_offset_y = 0

    def select_next_from_list(self, l, mod=1):
        logger.debug("selecting next from list %s" % (str(l)))
        if l:
            self.tab_counter += ( 1 * mod )
            if self.tab_counter > len(l) - 1:
                self.tab_counter = 0
            if self.tab_counter < 0:
                self.tab_counter = len(l) - 1
            choice = l[self.tab_counter]
            self.select_image(choice)
            return self.focused_image
        return None      

    def select_next_image(self, near, x, y):
        selected = self.select_next_from_list(near)
        if selected:
            logger.debug("selected a new image! %s" % selected)
            return selected
        else:
            logger.debug("nothing selected!")
        return None

    def select_prev_image(self, near, x, y):
        selected = self.select_next_from_list(near, -1)
        if selected:
            logger.debug("selected a new image! %s" % selected)
            return selected
        else:
            logger.debug("nothing selected!")
        return None

    def select_image(self, n):
        logging.debug("selecting new image %d" % n)
        self.focused_image = n
        self.picked_up = True
