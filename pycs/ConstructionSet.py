import PySimpleGUI as sg
from pycs.CanvasImageViewer import CanvasImageViewer
from pycs.WorldModel import WorldModel
from pycs.ImageCollection import ImageCollection
from tkinter import PhotoImage
from PIL import Image, ImageTk

class ConstructionSetApp:

    def __init__(self, wm: WorldModel, image_viewer: CanvasImageViewer, ic: ImageCollection):

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

        self.canvasx0 = self.canvas.canvasx(0)
        self.canvasy0 = self.canvas.canvasy(0)

        WIN_W, WIN_H = self.window.size

        # Fix sizes
        self.window_canvas.set_size((int(WIN_W),int(WIN_H) * self.CANVAS_PROP))

        # Get data
        self.wm = wm

        # Define a highlight object
        self.highlight = self.canvas.create_rectangle(0, 0, 0, 0, outline='red', width=10)

        # Create object to store image data 
        # Create object to store index between canvas image and world model
        self.photo_images = []
        self.wi2ci = {} 
        self.ci2wi = {}
        for wi, ent in enumerate(wm.world_objects):
            tmpgif = ImageTk.PhotoImage(Image.open(ent.png).resize((ent.w, ent.h)))
            self.photo_images.append(tmpgif)
#            ci = self.canvas.create_image(ent.x + self.canvasx0, ent.y + self.canvasy0, image=tmpgif, anchor="nw")
            ci = self.canvas.create_image(ent.x, ent.y, image=tmpgif, anchor="nw")
            self.wi2ci[wi] = ci 
            self.ci2wi[ci] = wi

        self.selector = ImageSelector()
        
        # Get camera
        self.camera = CanvasCamera(self.WIDTH * self.CANVAS_PROP, self.HEIGHT * self.CANVAS_PROP)

        # Canvas bindings, have to be directly to the Tk object or wont work

        def click_m1(event):
            print(event)
            x, y = event.x, event.y
            print("canvasa winfo vs!", self.canvas.winfo_pointerx(), self.root.winfo_pointerx())
            self.selector.click(self.root.winfo_pointerx(), self.root.winfo_pointery())
            nearest = self.wi2ci[self.wm.find_nearest(x, y)]
            self.selector.select_image(nearest)
            

        def release_m1(event):
            self.selector.release()

        def bring_forward(event):
            self.canvas.lift(self.highlight)
            self.canvas.lift(self.selector.focused_image)
    
        def send_backward(event):
            self.canvas.lower(self.selector.self.focused_image)
            self.canvas.lower(self.highlight)

        def tab_func(event):
            x, y = event.x, event.y
            print("PRESSTATE", event.state, event.keysym)
            if event.state == "Shift":
                print("AHHHHHHHHHHHHSHIFT")
            print("pressed tab", self.root.winfo_pointerx(), self.canvasx0, self.root.winfo_pointerx() - self.canvasx0)
            near = self.wm.find_near(x, y)
            cnear = [self.wi2ci[i] for i in near]
            self.selector.select_next_image(cnear, x, y)
            self.move_highlight_to_image(self.selector.focused_image)

        def shift_tab_func(event):
            x, y = event.x, event.y
            print("pressed tab", self.root.winfo_pointerx(), self.canvasx0, self.root.winfo_pointerx() - self.canvasx0)
            near = self.wm.find_near(x, y)
            cnear = [self.wi2ci[i] for i in near]
            self.selector.select_prev_image(cnear, x, y)
            self.move_highlight_to_image(self.selector.focused_image)

        def debug(event):
            print(event)

        self.canvas.bind('<KeyPress>', debug)
        self.canvas.bind('<Button-1>', click_m1)
        self.canvas.bind("<ButtonRelease-1>",release_m1)
        self.canvas.bind('<Tab>', tab_func)
        self.canvas.bind('<ISO_Left_Tab>', shift_tab_func)
        self.window.bind('<Configure>',"Configure")
        self.canvas.bind('<Up>', bring_forward)
        self.canvas.bind('<Down>', send_backward)

    def find_nearest(self, x, y):
        found = self.canvas.find_closest(x, y, halo=2, start=0)
        return found[0]

    def move_highlight_to_image(self, image_n):
        # rename function if it selects and highlights
        coords = self.canvas.coords(image_n)
        print("moving highlight to image", image_n, "at",  coords)
        x, y = coords
        self.move_highlight(x, y,
                           x + self.photo_images[self.ci2wi[self.selector.focused_image]].width(), 
                           y + self.photo_images[self.ci2wi[self.selector.focused_image]].height())


    def select_image(self, n):
        self.selector.select_image(n)
        print("!!", n)
        x, y = self.canvas.coords(n)
        self.move_highlight(x, y,
                           x + self.photo_images[self.selector.focused_image].width(), 
                           y + self.photo_images[self.selector.focused_image].height())

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

    def move_object(self):
        photo_image = self.photo_images[self.ci2wi[self.selector.focused_image]]
        canvas_image = self.selector.focused_image

        currx = self.root.winfo_pointerx()
        curry = self.root.winfo_pointery()

        dx = - (self.selector.origin_x - currx)
        dy = - (self.selector.origin_y - curry)

        self.selector.origin_x = currx
        self.selector.origin_y = curry
        x, y = self.canvas.coords(canvas_image)

        new_x = x + dx
        new_y = y + dy

        self.canvas.moveto(canvas_image, new_x, new_y)
        x, y = self.canvas.coords(canvas_image)
        
        self.canvas.coords(self.highlight, x, y, 
                            x + photo_image.width(), 
                            y + photo_image.height())
    
        self.wm.update_object_x(self.ci2wi[self.selector.focused_image], new_x)
        self.wm.update_object_y(self.ci2wi[self.selector.focused_image], new_y)



    def start(self):
        # Main loop

        # Main loop
        while True:
            if self.selector.picked_up:
                # tmp
                self.move_object()
                
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

