import PySimpleGUI as sg
import tkinter

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("cs." + __name__)

from pycs.interfaces.WorldModelABC import WorldModelABC
from pycs.CanvasImageCollection import CanvasImageCollection

class ConstructionSetApp:

    def __init__(self, wm: WorldModelABC):

        self.WIDTH, self.HEIGHT = sg.Window.get_screen_size()
        self.CANVAS_PROP = 0.95
        self.OUTPUT_PROP = 0.2

        sg.theme('dark grey 13')
        sg.set_options(element_padding=(0, 0))

        # Menu
        self.top_menu = [['&File', ['&Open', '&Save', '&Save As', '&Properties', 'E&xit' ]],
                    ['&Edit', ['&Paste', ['Special', 'Normal',], 'Undo'],],
                    ['&Toolbar', ['---', 'Foo &1', 'Bar &2', '---', 'Baz &3', 'FooBaz &4']],
                    ['&Help', '&About'],]

        self.right_click_menu = ['Unused', ['&New Object', '&Delete Object' '&Exit', 'Properties']]


        # GUI
        self.layout = [
                  [sg.MenubarCustom(self.top_menu, tearoff=False)],
                  [sg.Canvas(size=(self.WIDTH, self.HEIGHT * self.CANVAS_PROP), key='canvas', background_color='white')],
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

        # Create an image viewer to manipulate images on the canvas
        self.image_collection = CanvasImageCollection(self.canvas, 0, 0)

        # Create object to store image data 
        # Create object to store index between canvas image and world model
        self.wi2ci = {} 
        self.ci2wi = {}
        for wi, ent in enumerate(wm.world_objects):
            logger.debug("adding entity with dimensions %d %d %d %d" % (ent.x, ent.y, ent.w, ent.h))
            ci = self.image_collection.add_image(ent.png, ent.x, ent.y, ent.w, ent.h, anchor="nw")
            self.wi2ci[wi] = ci 
            self.ci2wi[ci] = wi

        # Input config
        self.m1_depressed = False

        # Canvas bindings, have to be directly to the Tk object or wont work
        def click_m1(event):
            logger.debug(event)
            self.m1_depressed = True
            x, y = event.x, event.y
            self.image_collection.click(self.root.winfo_pointerx(), self.root.winfo_pointery())
            nearest = self.wm.find_nearest(x, y)
            self.image_collection.select_image(nearest) 
            # add to command history

        def release_m1(event):
            self.m1_depressed = False
            self.image_collection.release()

        def bring_forward(event):
            # TODO: z index needs to be defined by the worldmodel too
            logger.debug("bringing object forward")
            self.image_collection.lift_focused_image()
    
        def send_backward(event):
            # TODO: z index needs to be defined by the worldmodel too
            logger.debug("sending object backward")
            self.image_collection.lower_focused_image()

        def tab_func(event):
            x, y = event.x, event.y
            near = self.wm.find_near(x, y)
            self.image_collection.select_next_image(near, x, y)

        def shift_tab_func(event):
            x, y = event.x, event.y
            near = self.wm.find_near(x, y)
            self.image_collection.select_prev_image(near, x, y)

        def duplicate_object(event):
            logger.debug("duplicating object")
            x, y = event.x, event.y
            i = self.image_collection.get_selected()
            wo = self.wm.duplicate_world_object(i, x, y)
            tmp_image = self.image_collection.add_image(wo.png, x, y, w=wo.w, h=wo.h, anchor="nw")

        def debug(event):
            logger.debug(event)

        def save(event):
            self.wm.save()
   

        self.canvas.bind('<KeyPress>', debug)
        self.canvas.bind('<Button-1>', click_m1)
        self.canvas.bind("<ButtonRelease-1>",release_m1)
        self.canvas.bind('<Tab>', tab_func)
        self.canvas.bind('<ISO_Left_Tab>', shift_tab_func)
        self.canvas.bind('<KeyPress-D>', duplicate_object)
        self.canvas.bind('<Control-KeyPress-s>', save)
        self.canvas.bind('<Up>', bring_forward)
        self.canvas.bind('<Down>', send_backward)
#        self.window.bind('<KeyPress-D>', "")
        self.window.bind('<Configure>',"Configure")

        self.canvas.focus_set()


    def find_nearest(self, x, y):
        found = self.canvas.find_closest(x, y, halo=2, start=0)
        return found[0]


#    def select_image(self, n):
#        self.image_selector.select_image(n)
#        logger.debug("!!", n)
#        x, y = self.canvas.coords(n)
#        self.move_highlight(x, y,
#                           x + self.photo_images[self.image_selector.focused_image].width(), 
#                           y + self.photo_images[self.image_selector.focused_image].height())

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
        while True:
            if self.m1_depressed:
                # tmp
                currx = self.root.winfo_pointerx()
                curry = self.root.winfo_pointery() 
                new_x, new_y = self.image_collection.move_selected_image(currx, curry)
                selected_image = self.image_collection.get_selected()
                self.wm.update_object_x(selected_image, new_x)
                self.wm.update_object_y(selected_image, new_y)

                
            WIN_W, WIN_H = self.window.size

            event, values = self.window.read()
            print(event, values)
            if event is None or event == 'Exit':
                return
            
            # Menu
            if event == 'About':
                self.window.disappear()
                sg.popup('about','version bar', 'baz', grab_anywhere=True)
                self.window.reappear()
            elif event == 'Open':
                sfilename = sg.popup_get_file('file to open', no_window=True)
            elif event == 'Save':
                self.wm.save()
            elif event == 'Save As':
#                sfilename = tkinter.filedialog.asksaveasfilename()
                sfoldername = sg.popup_get_folder('folder to open', no_window=True)
                if sfoldername:
                    logger.debug("saving! %s" % sfoldername)
                    self.wm.save(sfoldername)
            elif event == 'New Object':
                sfilename = sg.popup_get_file('image file', no_window=True)
                x, y = self.root.winfo_pointerx(), self.root.winfo_pointery()
                tmp_image = self.image_collection.add_image(sfilename, x, y, anchor="nw")
                tmpw, tmph = self.image_collection.get_image_dimensions(tmp_image)
                wo = self.wm.new_world_object("test", sfilename, x, y, w=tmpw, h=tmph)
            elif event == 'Delete Object':
                i = self.image_collection.get_selected()
                self.wm.delete_object(i)
                self.image_collection.delete_object(i)
                
            elif event == 'Properties':
                second_window()
            elif event == '-BMENU-':
                pass
            elif event == 'Configure':
                self.window_canvas.set_size((int(WIN_W),int(WIN_H) * self.CANVAS_PROP))

