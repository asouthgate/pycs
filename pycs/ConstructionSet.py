import PySimpleGUI as sg
import tkinter
import sys

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("cs." + __name__)

from pycs.interfaces.WorldModelABC import WorldModelABC
from pycs.CanvasImageCollection import CanvasImageCollection
from pycs.CommandExecutor import CommandExecutor
import pycs.CSCommands as pycsCom

class ConstructionSetApp:

    def __init__(self, wm: WorldModelABC):

        # Some required constants
        self._WIDTH, self._HEIGHT = sg.Window.get_screen_size()
        self._CANVAS_PROP = 0.95
        # A hack
        self._CANVAS_ORIGIN = 0

        # Some configuration
        sg.theme('dark grey 13')
        sg.set_options(element_padding=(0, 0))

        # Define menu elements
        self.top_menu = [
                    ['&File', ['&Open', '&Save', '&Save As', '&Properties', 'E&xit' ]],
                    ['&Edit', ['&Paste', ['Special', 'Normal'], 'Undo']],
                    ['&Toolbar', ['---', 'Foo &1', 'Bar &2', '---', 'Baz &3', 'FooBaz &4']],
                    ['&Help', '&About'],
                    ]

        self.right_click_menu = [
                    'Unused', ['&New Object', '&Delete Object' '&Exit', 'Properties'],
                    ]

        # Define layout
        self.layout = [
                  [sg.MenubarCustom(self.top_menu, tearoff=False)],
                  [sg.Canvas(size=(self._WIDTH, self._HEIGHT * self._CANVAS_PROP), key='canvas', background_color='white')],
                  ]

        # Create a window
        self.window = sg.Window(
                           "Construction Set",
                            self.layout,
                            default_element_size=(12, 1),
                            grab_anywhere=True,
                            right_click_menu=self.right_click_menu,
                            default_button_element_size=(12, 1),
                            resizable=True,finalize=True
                            )

        # Get some extra data structures under window
        self.root = self.window.TKroot
        self.window_canvas = self.window['canvas']
        self.canvas = self.window_canvas.TKCanvas

        # Fix sizes
        WIN_W, WIN_H = self.window.size
        self.window_canvas.set_size( ( int(WIN_W), int(WIN_H) * self._CANVAS_PROP ) )

        # Get data
        self.world_model = wm

        # Create an image viewer to manipulate images on the canvas
        self.image_collection = CanvasImageCollection(self.canvas, 0, 0)

        # Add images to the image collection
        for wi, ent in enumerate(wm.world_objects):
            logger.debug("adding entity with dimensions %d %d %d %d" % (ent.x, ent.y, ent.w, ent.h))
            ci = self.image_collection.add_image(ent.png, ent.x, ent.y, ent.w, ent.h, anchor="nw")

        # Create a command executor to handle input commands
        self.command_executor = CommandExecutor()

        # Define some state required for more complex inputs
        self.m1_depressed = False
        self.canvasx0 = self.canvas.canvasx(0)
        self.canvasy0 = self.canvas.canvasy(0)

        # Register inpupt callback functions
        # TODO: Refactor: Extract Function?
        def bind_inputs():            
            self.canvas.bind('<KeyPress>', self._debug)
            self.canvas.bind('<Button-1>', self._click_m1)
            self.canvas.bind("<ButtonRelease-1>", self._release_m1)
            self.canvas.bind('<Tab>', self._select_next_image)
            self.canvas.bind('<ISO_Left_Tab>', self._select_prev_image)
            self.canvas.bind('<KeyPress-D>', self._duplicate_selected_object)
            self.canvas.bind('<Control-KeyPress-s>', self._save)
            self.canvas.bind('<Control-KeyPress-z>', lambda e: self.command_executor.undo())
            self.canvas.bind('<Control-Shift-KeyPress-z>', lambda e: self.command_executor.redo())
            self.canvas.bind('<Up>', self._lift_selected)
            self.canvas.bind('<Down>', self._lower_selected)
            self.window.bind('<Configure>',"Configure")  
        bind_inputs()

        # Set focus to the canvas so input works properly from the get go
        self.canvas.focus_set()

        # Finally store the exit condition
        self._should_exit = False

    def _spawn_input_form(self):
        """ Define a second window GUI element for receiving input. """
        layout = [
                [sg.Canvas(size=(100, 100), key='canvas')],
                [sg.Text('foobarbaz')],
                [sg.OK()],
                ]
        window = sg.Window('Foo', layout)
        event, values = window.read()
        window.close()

    def _get_canvas_cursor_coords(self):
        """ Get position of the cursor consistent with calls to move objects """
        currx = self.root.winfo_pointerx()
        curry = self.root.winfo_pointery()
        logger.debug("Winfo_pointer = %s, Canvas coordinate = %s" % (currx, self.canvas.canvasx(currx)))
        return currx, curry - self._CANVAS_ORIGIN

    # Canvas bindings, have to be directly to the Tk object or wont work
    def _click_m1(self, event):
        """ User clicks a point; trigger downstream events and make a record of the position. """
        logger.debug(event)

        # A hack :(, near no way to get the canvas origin otherwise
        if not self._CANVAS_ORIGIN:
            x, y = self._get_canvas_cursor_coords()
            self._CANVAS_ORIGIN = y - event.y 

        # Log that m1 is depressed
        self.m1_depressed = True
        
        # Get the position of the cursor
        x, y = self._get_canvas_cursor_coords()

        # Register the click with the image_collection
        self.image_collection.click(x, y)

        # Find the nearest world object
        nearest = self.world_model.find_nearest(x, y)
        
        # Select the nearest image corresponding to it
        selected_image = self.image_collection.select_image(nearest) 
    
        # Execute the command
        command = pycsCom.ComFinishMove(self.image_collection, self.world_model, x, y, self.image_collection.get_selected())
        self.command_executor.execute(command)

    def _release_m1(self, event):
        self.m1_depressed = False
        self.image_collection.release()

    def _lift_selected(self, event):
        """ Bring the currently selected object forward. """
        # TODO: z index needs to be defined by the worldmodel too
        logger.debug("bringing object forward")
        command = pycsCom.ComLiftSelected(self.image_collection)
        self.command_executor.execute(command)

    def _lower_selected(self, event):
        """ Send the currently selected image backward. """
        # TODO: z index needs to be defined by the worldmodel too
        logger.debug("sending object backward")
        command = pycsCom.ComLowerSelected(self.image_collection)
        self.command_executor.execute(command)

    def _select_next_image(self, event):
        """ Select the 'next' image near the cursor. """
        x, y = event.x, event.y
        near = self.world_model.find_near(x, y)
        self.image_collection.select_next_image(near, x, y)

    def _select_prev_image(self, event):
        """ Select the 'prev' image near the cursor. """
        x, y = event.x, event.y
        near = self.world_model.find_near(x, y)
        self.image_collection.select_prev_image(near, x, y)

    def _duplicate_selected_object(self, event):
        """ Duplicate the currently selected object. """
        logger.debug("duplicating object")
        x, y = event.x, event.y
        i = self.image_collection.get_selected()
        command = pycsCom.ComDuplicate(self.image_collection, self.world_model, i, x, y)
        self.command_executor.execute(command)

    def _debug(self, event):
        logger.debug(event)

    def _show_about(self):
        self.window.disappear()
        sg.popup('about','version bar', 'baz', grab_anywhere=True)
        self.window.reappear()

    def _open_file(self):
        sfilename = sg.popup_get_file('file to open', no_window=True)

    def _save(self, *args):
        self.world_model.save()

    def _save_as(self):
        sfoldername = sg.popup_get_folder('folder to open', no_window=True)
        if sfoldername:
            logger.debug("saving! %s" % sfoldername)
            self.world_model.save(sfoldername)

    def _new_object(self):
        sfilename = sg.popup_get_file('image file', no_window=True)
        x, y = self._get_canvas_cursor_coords()
        tmp_image = self.image_collection.add_image(sfilename, x, y, anchor="nw")
        tmpw, tmph = self.image_collection.get_image_dimensions(tmp_image)
        wo = self.world_model.new_world_object("test", sfilename, x, y, w=tmpw, h=tmph)

    def _delete_object(self):
        i = self.image_collection.get_selected()
#        self.world_model.delete_object(i)
#        self.image_collection.delete_object(i)

    def _configure(self):
        WIN_W, WIN_H = self.window.size
        self.window_canvas.set_size( ( int(WIN_W), int(WIN_H) * self._CANVAS_PROP ) )

    def _process_events(self):
    
        logger.debug("Processing events")

        # Move object if necessary
        if self.m1_depressed:
            currx, curry = self._get_canvas_cursor_coords()
            command = pycsCom.ComFinishMove(self.image_collection, self.world_model, currx, curry, self.image_collection.get_selected())
            self.command_executor.pop_execute(command)
            
        logger.debug("Reading from the window")

        event, values = self.window.read()

        logger.debug("Read from the window")


        if self.should_exit: return

        # If no new event can be read, just exit
        if event is None or event == 'Exit':
            self._should_exit = True
        
        # Menu selections
        # TODO: replace with dict
        if event == 'About':
            self._show_about()

        elif event == 'Open':
            self._open_file()

        elif event == 'Save':
            self._save()

        elif event == 'Save As':
            self._save_as()

        elif event == 'New Object':
            self._new_object()
            
        elif event == 'Delete Object':
            self._delete_object()
            
        elif event == 'Properties':
            self._spawn_input_form()

        elif event == '-BMENU-':
            pass

        elif event == 'Configure':
            self._configure()

        return True

    def start(self):
        """ Start the apaplication! """

        while not self.should_exit:
            logger.debug("Checking whether we should exit!")
            self._process_events()
            logger.debug(self.command_executor)

    def exit(self):
        logger.debug("Exiting!")
        self._should_exit = True
        self.root.quit()

    @property
    def should_exit(self):
        return self._should_exit

