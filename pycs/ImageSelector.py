class ImageSelector:
    """ 
    Class responsible for selection of objects
    """
    def __init__(self):
        self.focused_image = 2
        self.tab_counter = 0
        self.origin_x = None
        self.origin_y = None
        self.picked_up = False
        self.canvas = canvas
        self.highlight = self.canvas.create_rectangle(0, 0, 0, 0, outline='red', width=10)

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
            print("selected a new image!", selected)
            return selected
        else:
            print("nothing selected!")
        return None

    def select_prev_image(self, near, x, y):
        selected = self.select_next_from_list(near, -1)
        if selected:
            print("selected a new image!", selected)
            return selected
        else:
            print("nothing selected!")
        return None

    def select_image(self, n):
        self.focused_image = n
        self.picked_up = True

    def get_selected_image_coords(self, canvas):
        x, y = canvas.coords(self.focused_image)
        return x, y    

