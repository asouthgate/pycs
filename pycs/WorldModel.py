import json
import random
from PIL import ImageTk

class WorldObject:
    def __init__(self, name, png, x, y, w, h):
        self.name = name
        self.png = png
        self.x = x
        self.y = y
        self.w = w
        self.h = h        

class WorldModel:

    def __init__(self):
#        self.gif1 = ImageTk.PhotoImage(Image.open('nicholas-taggart-wfp-dragon.gif').resize((100,100)))
#        self.image = self.canvas.create_image(0, 0, image=self.gif1, anchor="nw")

        self.entities = []
        for j in range(100):
            size = random.randint(20,100) 
            self.entities.append(WorldObject('Dragon', 'tmp_gif.gif', random.randint(0,1000), random.randint(0,500), size, size))

    def __inter__(self):
        for ent in self.entities:
            yield ent

    def __getitem__(self, x):
        pass
   
    def __setitem__(self, x, v):
        pass

    def _index(self):
        # fast spatial index for retrieving objects
        pass
        
    def query(self, v_ul, v_br):
        # query for objects in box between v_ul and v_br
        pass
        
