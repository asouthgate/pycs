import PySimpleGUI as sg
#from pycs.CameraCanvas import CameraCanvas
#from pycs.GameWorld import GameWorld
from tkinter import PhotoImage
from PIL import Image, ImageTk


WIDTH, HEIGHT = sg.Window.get_screen_size()

CANVAS_PROP = 0.7
OUTPUT_PROP = 0.2

def second_window():
    layout = [
            [sg.Canvas(size=(100, 100), key='canvas')],
            [sg.Text('foobarbaz')],
              [sg.OK()]]
    window = sg.Window('Foo', layout)
    event, values = window.read()
    window.close()

def main():

    sg.theme('DarkAmber')
    sg.set_options(element_padding=(0, 0))

    # Menu
    top_menu = [['&File', ['&Open', '&Save', '&Properties', 'E&xit' ]],
                ['&Edit', ['&Paste', ['Special', 'Normal',], 'Undo'],],
                ['&Toolbar', ['---', 'Foo &1', 'Bar &2', '---', 'Baz &3', 'FooBaz &4']],
                ['&Help', '&About'],]

    right_click_menu = ['Unused', ['!&Foo', '&Exit', 'Properties']]


    # GUI
    layout = [
              [sg.MenubarCustom(top_menu, tearoff=False)],
              [sg.Canvas(size=(WIDTH, HEIGHT*CANVAS_PROP), key='canvas', background_color='white')],
              [sg.Output(size=(WIDTH, HEIGHT*OUTPUT_PROP), echo_stdout_stderr=True)],
              ]

    # Window
    window = sg.Window("Construction Set",
                       layout,
                       default_element_size=(12, 1),
                       grab_anywhere=True,
                       right_click_menu=right_click_menu,
                       default_button_element_size=(12, 1),
                       resizable=True,finalize=True)


    root = window.TKroot
    canvas = window['canvas']
    gif1 = ImageTk.PhotoImage(Image.open('nicholas-taggart-wfp-dragon.gif').resize((100,100)))
    image = canvas.TKCanvas.create_image(0, 0, image=gif1, anchor="nw")

    # Canvas bindings, have to be directly to the Tk object or wont work
    # Probably we should rap a reference to this with functionality
#    canvas.TKCanvas.bind('<Motion>', get_coordinates)
    global picked_up
    picked_up = False
    def click_m1(event):
        global picked_up
        picked_up = True
        print("\t CLICK", event)
    def release_m1(event):
        global picked_up
        print("\tRELEASE",picked_up)
        if picked_up:
            print("moving!")
            picked_up=False
            pass
        print("\t RELEASE", event)
    canvas.TKCanvas.bind('<Button-1>', click_m1)
    canvas.TKCanvas.bind("<ButtonRelease-1>",release_m1)

    window.bind('<Configure>',"Configure")


    # Main loop
    while True:
        if picked_up:
            x = root.winfo_pointerx() - root.winfo_rootx() - gif1.width()
            y = root.winfo_pointery() - root.winfo_rooty() - gif1.height()
            canvas.TKCanvas.moveto(image, x, y)
            
        WIN_W, WIN_H = window.size

        event, values = window.read()
        if event is None or event == 'Exit':
            return
        if event == "Motion":
            print("Motion", event, values)
            print("GOT MOTION", x, y)
        
        # Menu
        if event == 'About':
            window.disappear()
            sg.popup('about','version bar', 'baz', grab_anywhere=True)
            window.reappear()
        elif event == 'Open':
            filename = sg.popup_get_file('file to open', no_window=True)
#            print(filename)
        elif event == 'Properties':
            second_window()
        elif event == '-BMENU-':
            pass
#            print('Button menu selection:', values['-BMENU-'])
        elif event == 'Configure':
#            print("config event, new size:", WIN_W, WIN_H)
            canvas.set_size((int(WIN_W),int(WIN_H) * CANVAS_PROP))


if __name__ == "__main__":
    main()
