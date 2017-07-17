import tkinter
import actions
rootWidth = 500
rootHeight = 150

sliderWidth = 400
sliderHeight = 70

buttonWidth = 50
buttonHeight = 20

viewFrame = 0


def generateParentWindow(Frame):
    # Set the properties of the parent window here
    Frame.title("FocusApp")
    # Frame.geometry("500x150")
    Frame.geometry(str(rootWidth) + "x" + str(rootHeight))
    # Attach the logo here
    img = tkinter.PhotoImage(file='favicon.gif')
    Frame.tk.call('wm', 'iconphoto', Frame._w, img)
    return Frame

def generateSlider(Frame):
    # Add label here
    w = tkinter.Label(Frame, text="Time (in hours)")
    # w.place(x = (rootWidth - sliderWidth)/2, y = 10, width=sliderWidth, height=sliderHeight)
    w.pack()
    w2 = tkinter.Scale(Frame, from_=0, to=24, length=sliderWidth, resolution=0.5, orient="horizontal")
    # w2.grid(row=5, column=10)
    w2.set(23)
    # w2.pack()
    w2.place(x = (rootWidth - sliderWidth)/2, y = 20, width=sliderWidth, height=sliderHeight)

def generateStartButton(Frame):
    b = tkinter.Button(Frame, text ="Start", command = actions.startButtonAction)
    # .grid(row=7, column=10)

    # b.pack(side="left")
    b.place(x = (rootWidth - buttonWidth)/2 - 2 * buttonWidth, y = sliderHeight + buttonHeight, width=buttonWidth, height=buttonHeight)

def generateViewButton(Frame):
    b = tkinter.Button(Frame, text ="View", command = actions.viewButtonAction)
    # .grid(row=7, column=18)
    # b.pack(side="right")
    b.place(x = (rootWidth - buttonWidth)/2  + 2 * buttonWidth, y = sliderHeight + buttonHeight, width=buttonWidth, height=buttonHeight)

def hello():
    print("Called hello --> ")

def generateViewSitesFrame():
    # Display a new frame here
    global viewFrame
    viewFrame = tkinter.Toplevel()
    viewFrame.title("FocusApp - Sites list")
    viewFrame.geometry(str(rootWidth) + "x" + str(rootHeight))
    img = tkinter.PhotoImage(file='favicon.gif')
    viewFrame.tk.call('wm', 'iconphoto', viewFrame._w, img)
    # Add an Entry widget 
    entry = tkinter.Entry(viewFrame)
    entry.pack()
    # Add an Add button here
    addButton = tkinter.Button(viewFrame, text ="Add", command = actions.addButtonAction)
    # .grid(row=7, column=10)

    # b.pack(side="left")
    # addButton.place(x = (rootWidth - buttonWidth)/2 - 2 * buttonWidth, y = sliderHeight + buttonHeight, width=buttonWidth, height=buttonHeight)
    addButton.pack()

    # Create a listbox here
    lb = tkinter.Listbox(viewFrame)
    # Open the domains.list file here and populate the entries
    lb.insert(1, "hey")
    lb.pack()

    # Add a context menu here
    # create a popup menu
    menu = tkinter.Menu(viewFrame, tearoff=0)
    menu.add_command(label="Undo", command=hello)
    menu.add_command(label="Redo", command=hello)

    # create a canvas
    frame = tkinter.Frame(viewFrame, width=512, height=512)
    frame.pack()

    def popup(event):
        menu.post(event.x_root, event.y_root)
        # print(event.x_root, event.y_root)
        w = event.widget

        print(w.curselection())
        print()

        index = int(w.curselection()[0])
        value = w.get(index)

        print('You selected item %d: "%s"' % (index, value))
        print()

    # attach popup to canvas
    lb.bind("<Button-3>", popup)

    
    

    # return viewFrame