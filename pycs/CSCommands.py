from pycs.interfaces.CommandABC import CommandABC

class ComLowerSelected(CommandABC):

    def __init__(self, image_collection):
        self.image_collection = image_collection
        self.focused_image = self.image_collection.get_selected()

    def execute(self):
        self.image_collection.select_image(self.focused_image)
        self.image_collection.lower_focused_image()

    def undo(self):
        self.image_collection.select_image(self.focused_image)
        self.image_collection.lift_focused_image()

class ComLiftSelected(CommandABC):

    def __init__(self, image_collection):
        self.image_collection = image_collection
        self.focused_image = self.image_collection.get_selected()

    def execute(self):
        self.image_collection.select_image(self.focused_image)
        self.image_collection.lift_focused_image()

    def undo(self):
        self.image_collection.select_image(self.focused_image)
        self.image_collection.lower_focused_image()
       
