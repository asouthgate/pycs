import PySimpleGUI as sg
from pycs.CameraCanvas import CameraCanvas
from pycs.WorldModel import WorldModel
from tkinter import PhotoImage
from PIL import Image, ImageTk

class ConstructionSetApp:

    def __init__(self):

        self.WIDTH, self.HEIGHT = sg.Window.get_screen_size()
        self.CANVAS_PROP = 0.7
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
                  [sg.Output(size=(self.WIDTH, self.HEIGHT * self.OUTPUT_PROP), echo_stdout_stderr=True)],
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


        self.gif1 = ImageTk.PhotoImage(Image.open('nicholas-taggart-wfp-dragon.gif').resize((100,100)))
        self.image = self.canvas.create_image(0, 0, image=self.gif1, anchor="nw")

        # Canvas bindings, have to be directly to the Tk object or wont work
        # Probably we should rap a reference to this with functionality
    #    canvas.TKCanvas.bind('<Motion>', get_coordinates)

        self.picked_up = False
        def click_m1(event):
            self.picked_up = True
            print("\t CLICK", event)

        def release_m1(event):
            print("\tRELEASE", self.picked_up)
            if self.picked_up:
                print("moving!")
                self.picked_up = False
            print("\t RELEASE", event)

        self.canvas.bind('<Button-1>', click_m1)
        self.canvas.bind("<ButtonRelease-1>",release_m1)
        self.window.bind('<Configure>',"Configure")

    def second_window(self):
        layout = [
                [sg.Canvas(size=(100, 100), key='canvas')],
                [sg.Text('foobarbaz')],
                  [sg.OK()]]
        window = sg.Window('Foo', layout)
        event, values = window.read()
        window.close()

    def main(self):

        # Main loop
        while True:
            if self.picked_up:
                x = self.root.winfo_pointerx() - self.root.winfo_rootx() - self.gif1.width()
                y = self.root.winfo_pointery() - self.root.winfo_rooty() - self.gif1.height()
                self.canvas.moveto(self.image, x, y)
                
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
    ConstructionSetApp().main()
