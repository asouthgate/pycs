class CanvasCamera:

    def __init__(self, width, height):
        # Define box; note position is the bottom right of the box
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height        

    def zoom(self, dw, dh):
        # increase bounding box by dw, dh
        pass

    def pan(self, v):
        # move in direction v
        pass

    def get_objects_in_view(self, world_model):
        # return a list of objects that can be seen in the camera
        pass
