import PySimpleGUI as sg
from pycs.CameraCanvas import CanvasCamera
from pycs.WorldModel import WorldModel
from tkinter import PhotoImage
from PIL import Image, ImageTk

class ConstructionSetApp:

    def __init__(self):

        self.WIDTH, self.HEIGHT = sg.Window.get_screen_size()
        self.CANVAS_PROP = 0.95
        self.OUTPUT_PROP = 0.2

        sg.theme('DarkAmber')
        sg.set_options(element_padding=(0, 0))

        # Menu
        self.top_menu = [['&File', ['&Open', '&Save', '&Properties', 'E&xit' ]],
                    ['&Edit', ['&Paste', ['Special', 'Normal',], 'Undo'],],
                    ['&Toolbar', ['---', 'Foo &1', 'Bar &2', '---', 'Baz &3', 'FooBaz &4']],
                    ['&Help', '&About'],]

        self.right_click_menu = ['Unused', ['!&Foo', '&Exit', 'Properties']]


        # GUI
        self.layout = [
                  [sg.MenubarCustom(self.top_menu, tearoff=False)],
                  [sg.Canvas(size=(self.WIDTH, self.HEIGHT * self.CANVAS_PROP), key='canvas', background_color='white')],
#                  [sg.Output(size=(self.WIDTH, self.HEIGHT * self.OUTPUT_PROP), echo_stdout_stderr=True)],
                  ]

        # Window
        self.window = sg.Window("Construction Set",
                           self.layout,
                           default_element_size=(12, 1),
                           grab_anywhere=True,
                           right_click_menu=self.right_click_menu,
                           default_button_element_size=(12, 1),
                           resizable=True,finalize=True)


        # Get some extra data structures under window
        self.root = self.window.TKroot
        self.window_canvas = self.window['canvas']
        self.canvas = self.window_canvas.TKCanvas
        WIN_W, WIN_H = self.window.size

        # Fix sizes
        self.window_canvas.set_size((int(WIN_W),int(WIN_H) * self.CANVAS_PROP))


        # Get data
        self.wm = WorldModel()

        # TODO: make image picker object
        # Set image focused
        self.focused_image = 0
        self.tab_counter = 0
#        self.picker_offset_x = self.root.winfo_pointerx()
#        self.picker_offset_y = self.root.winfo_pointery()
        self.clicker_origin_x = None
        self.clicker_origin_y = None
        self.picked_up = False
        self.highlight = self.canvas.create_rectangle(0, 0, 0, 0, outline='red', width=10)

        # Initialize all images on the canvas
        self.canvas_images = []
        self.photo_images = []
        for ent in self.wm.entities:
            tmpgif = ImageTk.PhotoImage(Image.open(ent.png).resize((ent.w, ent.h)))
            self.photo_images.append(tmpgif)
            self.canvas_images.append(self.canvas.create_image(ent.x, ent.y, image=tmpgif, anchor="nw"))
        
        # Get camera
        self.camera = CanvasCamera(self.WIDTH * self.CANVAS_PROP, self.HEIGHT * self.CANVAS_PROP)

        # Canvas bindings, have to be directly to the Tk object or wont work

        def click_m1(event):
            self.picked_up = True
            self.clicker_origin_x = self.root.winfo_pointerx()
            self.clicker_origin_y = self.root.winfo_pointery()
            print("\t CLICK", event)

        def release_m1(event):
            print("\tRELEASE", self.picked_up)
            if self.picked_up:
                print("moving!")
                self.picked_up = False
                self.picker_offset_x = 0
                self.picker_offset_y = 0
            print("\t RELEASE", event)

        def select_next_image(event):
            near = self.find_near(self.root.winfo_pointerx(), self.root.winfo_pointery())
            self.tab_counter += 1
            if self.tab_counter > len(near) - 1:
                self.tab_counter = 0
            self.focused_image = near[self.tab_counter]
            print("focusing", self.focused_image)
            self.select_image(self.focused_image)

        def bring_forward(event):
            self.canvas.lift(self.highlight)
            self.canvas.lift(self.canvas_images[self.focused_image])
    
        def send_backward(event):
            self.canvas.lower(self.canvas_images[self.focused_image])
            self.canvas.lower(self.highlight)

        self.canvas.bind('<Button-1>', click_m1)
        self.canvas.bind("<ButtonRelease-1>",release_m1)
        self.canvas.bind('<Tab>', select_next_image)
        self.window.bind('<Configure>',"Configure")
        self.canvas.bind('<Up>', bring_forward)
        self.canvas.bind('<Down>', send_backward)

    def find_nearest(self, x, y):
        found = self.canvas.find_closest(x, y, halo=2, start=0)
        return found[0]

    def find_near(self, x, y, halo=50):
        found = self.canvas.find_overlapping(x - halo, y - halo, x + halo, y + halo)
        print(found)
        return found


    def highlight(self, image_n):
        x, y = self.canvas.coords(self.canvas_images[self.focused_image])
        self.move_highlight(x, y,
                           x + self.photo_images[self.focused_image].width(), 
                           y + self.photo_images[self.focused_image].height())


    def select_image(self, n):
        self.focused_image = n
        self.picked_up = True
        x, y = self.canvas.coords(self.canvas_images[self.focused_image])
        print(x, y)
        self.canvas.coords(self.canvas_images[self.focused_image], x, y)
#        self.move_highlight(x, y, 
        self.move_highlight(x, y,
                           x + self.photo_images[self.focused_image].width(), 
                           y + self.photo_images[self.focused_image].height())


    def move_highlight(self, x1, y1, x2, y2):
        self.canvas.coords(self.highlight, x1, y1, x2, y2)       

    def second_window(self):
        layout = [
                [sg.Canvas(size=(100, 100), key='canvas')],
                [sg.Text('foobarbaz')],
                  [sg.OK()]]
        window = sg.Window('Foo', layout)
        event, values = window.read()
        window.close()

    def start(self):
        # Main loop

        # Main loop
        while True:
            if self.picked_up:
                # tmp
                photo_image = self.photo_images[self.focused_image]
                canvas_image = self.canvas_images[self.focused_image]

#                x = self.root.winfo_pointerx() - self.root.winfo_rootx() - photo_image.width()
#                y = self.root.winfo_pointery() - self.root.winfo_rooty() - photo_image.height()
                dx = - (self.clicker_origin_x - self.root.winfo_pointerx())
                dy = - (self.clicker_origin_y - self.root.winfo_pointery())
                self.clicker_origin_x = self.root.winfo_pointerx()
                self.clicker_origin_y = self.root.winfo_pointery()
                x, y = self.canvas.coords(canvas_image)

                self.canvas.moveto(canvas_image, x + dx, y + dy)
                x, y = self.canvas.coords(canvas_image)
                
                self.canvas.coords(self.highlight, x, y, 
                                    x + self.photo_images[self.focused_image].width(), 
                                    y + self.photo_images[self.focused_image].height())
                
            WIN_W, WIN_H = self.window.size

            event, values = self.window.read()
            if event is None or event == 'Exit':
                return
            if event == "Motion":
                print("Motion", event, values)
                print("GOT MOTION", x, y)
            
            # Menu
            if event == 'About':
                self.window.disappear()
                sg.popup('about','version bar', 'baz', grab_anywhere=True)
                self.window.reappear()
            elif event == 'Open':
                sfilename = sg.popup_get_file('file to open', no_window=True)
    #            print(filename)
            elif event == 'Properties':
                second_window()
            elif event == '-BMENU-':
                pass
    #            print('Button menu selection:', values['-BMENU-'])
            elif event == 'Configure':
    #            print("config event, new size:", WIN_W, WIN_H)
                self.window_canvas.set_size((int(WIN_W),int(WIN_H) * self.CANVAS_PROP))


if __name__ == "__main__":
    ConstructionSetApp().start()
