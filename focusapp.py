import tkinter
import pathlib
import time

class FocusApp:
    """
    Class that stores the entire focus app
    """
    def __init__(self):
        """Initialises all the required variables"""
        self.rootWidth = 500
        self.rootHeight = 150
        self.sliderWidth = 400
        self.sliderHeight = 70
        self.buttonWidth = 50
        self.buttonHeight = 20
        self.timerBeingDisplayed = False

        # Start building the GUI here
        self.__generateParentWindow__()
        self.__generateSlider__()
        self.__generateStartButton__()
        self.__generateViewButton__()
        
    def __generateParentWindow__(self):
        """Creates the root window"""
        self.parentWindow = tkinter.Tk()
        self.parentWindow.title("FocusApp")
        self.parentWindow.geometry(str(self.rootWidth) + "x" + str(self.rootHeight))
        # Attach the logo here
        self.img = tkinter.PhotoImage(file='favicon.gif')
        self.parentWindow.tk.call('wm', 'iconphoto', self.parentWindow._w, self.img)
        
    def __generateSlider__(self):
        """Creates the slider present on the root window that enables time to be selected"""
        self.sliderLabel = tkinter.Label(self.parentWindow, text="Time (in hours)")
        # self.sliderLabel.place(x = (self.rootWidth - self.sliderWidth)/2, y = 10, width=self.sliderWidth, height=self.sliderHeight)
        self.sliderLabel.pack()
        self.slider = tkinter.Scale(self.parentWindow, from_=0, to=24, length=self.sliderWidth, resolution=0.5, orient="horizontal")
        # self.slider.grid(row=5, column=10)
        self.slider.set(23)
        # self.slider.pack()
        self.slider.place(x = (self.rootWidth - self.sliderWidth)/2, y = 20, width=self.sliderWidth, height=self.sliderHeight)

    def __generateStartButton__(self):
        """Creates the start button on the root window that will start the block"""
        self.startButton = tkinter.Button(self.parentWindow, text ="Start", command = self.startButtonAction)
        # .grid(row=7, column=10)

        # self.startButton.pack(side="left")
        self.startButton.place(x = (self.rootWidth - self.buttonWidth)/2 - 2 * self.buttonWidth, y = self.sliderHeight + self.buttonHeight, width=self.buttonWidth, height=self.buttonHeight)

    def __generateViewButton__(self):
        """Creates the view button on the root window that will display a sub-window that lists all the blocked sites"""
        self.viewButton = tkinter.Button(self.parentWindow, text ="View", command = self.viewButtonAction)
        # .grid(row=7, column=18)
        # self.viewButton.pack(side="right")
        self.viewButton.place(x = (self.rootWidth - self.buttonWidth)/2  + 2 * self.buttonWidth, y = self.sliderHeight + self.buttonHeight, width=self.buttonWidth, height=self.buttonHeight)

    def __generateEntryWidget__(self):
        """Creates the entry widget in the view-list window"""
        self.entry = tkinter.Entry(self.viewListWindow)
        self.entry.pack()
    
    def __generateAddButton__(self):
        """Creates the add button in the view-list window"""
        self.addButton = tkinter.Button(self.viewListWindow, text ="Add", command = self.addButtonAction)
        # .grid(row=7, column=10)

        # b.pack(side="left")
        # self.addButton.place(x = (rootWidth - buttonWidth)/2 - 2 * buttonWidth, y = sliderHeight + buttonHeight, width=buttonWidth, height=buttonHeight)
        self.addButton.pack()
        self.viewListWindow.bind("<Return>", self.__handleEnter__)
    
    def __handleEnter__(self, event):
        """This method is called when the RETURN key is pressed on the viewListWindow"""
        self.addButtonAction()

    def __generateListBox__(self):
        """Creates the listbox widget in the view-list window"""
        self.listBox = tkinter.Listbox(self.viewListWindow)
        self.__displayAllDomainsInListBox__()
        self.listBox.pack()
    
    def __generateListBoxContextMenu__(self):
        """Creates the context menu for the listbox in the view-list window"""
        # Add a context menu here
        # create a popup menu
        self.listboxContextMenu = tkinter.Menu(self.viewListWindow, tearoff=0)
        self.listboxContextMenu.add_command(label="Delete", command=self.deleteMenuAction)

        # create a canvas
        frame = tkinter.Frame(self.viewListWindow, width=512, height=512)
        frame.pack()

        def popup(event):
            # Check if selection has been made
            if event.widget.curselection() == ():
                return
            # Otherwise, don't display the menu
            # self.listboxContextMenu.post(event.x_root, event.y_root)
            self.listboxContextMenu.tk_popup(event.x_root, event.y_root)
        # attach popup to canvas
        self.listBox.bind("<Button-3>", popup)
    
    def __generateViewSitesFrame__(self):
        """Creates the sub-window that lists all the blocked sites"""
        self.viewListWindow = tkinter.Toplevel()
        self.viewListWindow.title("FocusApp - Sites list")
        self.viewListWindow.geometry(str(self.rootWidth) + "x" + str(self.rootHeight))
        self.viewListWindow.tk.call('wm', 'iconphoto', self.viewListWindow._w, self.img)

        self.__generateEntryWidget__()
        self.__generateAddButton__()
        self.__generateListBox__()
        self.__generateListBoxContextMenu__()
        
    def __displayAllDomainsInListBox__(self):
        """Parses through the domains.list file and loads all the domains into the listbox"""
        # Delete all the elements
        self.listBox.delete(0, tkinter.END)
        # Open the domains.list file here and populate the entries
        if not pathlib.Path("domains.list").is_file():
            # Create an domains.list file here
            open("domains.list", "w").close()
        # domains.list exists here
        domainsFile = open("domains.list", "r")
        domainsList = domainsFile.read().split("\n")
        i = 1
        for domain in domainsList:
            self.listBox.insert(i, domain)
            i += 1
        domainsFile.close()
        
    def start(self):
        """Starts the GUI"""
        # Read the .stats file.   
        if not pathlib.Path(".stats").is_file():
            # If no .stats file is present, start the mainloop.
            self.parentWindow.mainloop()
        else:
            # .stats file is present.
            # Read the endtime
            endTime = 0
            try:
                endTime = int(open(".stats", "r").read())
            except:
                endTime = 0
            currentTime = time.time()
            if currentTime > endTime:
                # If cur_time > endtime, start the mainloop.
                self.parentWindow.mainloop()
            else:
                # Otherwise, display a box with remaining time.
                self.displayTimer(endTime - currentTime)

    def displayTimer(timeLeft):
        """Method displays a timer"""
        if not self.timerBeingDisplayed:
            self.timerBeingDisplayed = True
            try:
                self.parentWindow.destroy()
            except:
                pass
        
        
    
    def startButtonAction(self):
        """Called when the start button is pressed"""
        print("Start button has been clicked!")
        # Fetch the time in the slider
        # Read all the sites in domains.list. If no domains.list file is present, display a messagebox stating so.
        # Create a .stats file, with endtime

        return

    def viewButtonAction(self):
        """Called when the view button is pressed. Will generate another window that will list all the sites that need to be blocked."""
        self.__generateViewSitesFrame__()
    
    def addButtonAction(self):
        """Called when the add button is clicked. This will add the value entered in the text field to the domains list."""
        # Get the value in the entry widget
        domain = self.entry.get()
        if domain == "":
            return
        # Clear the value in the entry widget
        self.entry.delete(0, tkinter.END)
        if not pathlib.Path("domains.list").is_file():
            # Create an domains.list file here
            open("domains.list", "w").close()
        # Read all domains
        domainsList = open("domains.list", "r").read().split("\n")
        # Prepend to the list
        domainsList.insert(0, domain)
        # Write to the file
        domainsFile = open("domains.list", "w")
        domainsFile.write("\n".join(domainsList))
        domainsFile.close()
        self.__displayAllDomainsInListBox__()

    def deleteMenuAction(self):
        """Called when the delete context menu is clicked"""
        value = self.listBox.get(self.listBox.curselection()[0])
        if value == "":
            return
        # Read the file and store all the elements in a list
        domainsList = open("domains.list", "r").read().split("\n")
        domainsList.remove(value)
        domainsFile = open("domains.list", "w")
        domainsFile.write("\n".join(domainsList))
        domainsFile.close()
        self.__displayAllDomainsInListBox__()

"""
TODO
4. Handle start button action. Once the process begins, destroy the parentWindow.
5. Use grid to restyle the app.
6. Display a timer in case the process had already started. Try to destroy the parentWindow.
7. After the timer ends, display the parent window.
8. While rewriting the /etc/hosts file, create a backup /etc/hosts.backup. Also write for IPv4 and IPv6.
"""