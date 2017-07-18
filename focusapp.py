try:
    import tkinter
except:
    import Tkinter as tkinter
import pathlib
import time
try:
    from tkinter import messagebox
except:
    import tkMessageBox
import shutil
import subprocess
import sys
import os.path

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


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
        self.parentWindow = tkinter.Tk()
        self.parentWindow.title("FocusApp")
        self.parentWindow.geometry(str(self.rootWidth) + "x" + str(self.rootHeight))
        # Attach the logo here
        self.img = tkinter.PhotoImage(file=resource_path('favicon.gif'))
        self.parentWindow.tk.call('wm', 'iconphoto', self.parentWindow._w, self.img)
        
    
    def __clearParentWindowCanvas__(self):
        """Method deletes all the child elements of the parentWindow node"""
        for child in self.parentWindow.winfo_children():
            try:
                child.destroy()
            except:
                pass
            # child.destroy()
        
    def __generateParentWindow__(self):
        """Creates the root window"""
        self.__clearParentWindowCanvas__()
        self.__generateSlider__()
        self.__generateStartButton__()
        self.__generateViewButton__()
        # Check if /etc/.hosts.backup already exists. If it does, then copy it back to /etc/hosts. Otherwise, do nothing
        
        
    def __generateSlider__(self):
        """Creates the slider present on the root window that enables time to be selected"""
        self.sliderLabel = tkinter.Label(self.parentWindow, text="Time (in hours)")
        # self.sliderLabel.place(x = (self.rootWidth - self.sliderWidth)/2, y = 10, width=self.sliderWidth, height=self.sliderHeight)
        self.sliderLabel.pack()
        self.slider = tkinter.Scale(self.parentWindow, from_=0.5, to=24, length=self.sliderWidth, resolution=0.5, orient="horizontal")
        # self.slider.grid(row=5, column=10)
        self.slider.set(0.5)
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
    
    def __generateTimerWindow__(self):
        """Creates a timer window that displays the time left before sites would be automatically unblocked"""
        self.__clearParentWindowCanvas__()

        # Add a label here
        self.timerWindowLabel = tkinter.Label(self.parentWindow, text="Hey")
        self.timerWindowLabel.pack()
        # self.timerWindow.mainloop()
        
    def __displayAllDomainsInListBox__(self):
        """Parses through the .domains.list file and loads all the domains into the listbox"""
        # Delete all the elements
        self.listBox.delete(0, tkinter.END)
        # Open the .domains.list file here and populate the entries
        if not pathlib.Path(".domains.list").is_file():
            # Create an .domains.list file here
            open(".domains.list", "w").close()
        # .domains.list exists here
        domainsFile = open(".domains.list", "r")
        domainsList = domainsFile.read().split("\n")
        i = 1
        for domain in domainsList:
            self.listBox.insert(i, domain)
            i += 1
        domainsFile.close()
    
    def __writeToHosts__(self):
        """Method reads the .domains.list file and writes to /etc/hosts"""
        domainsList = open(".domains.list", "r").read().split("\n")
        hostsFile = ""
        for domain in domainsList:
            if domain == "":
                continue
            hostsFile += "127.0.0.1 " + domain + "\n"
            hostsFile += "::1       " + domain + "\n\n"
        # print("Hosts file has become: \n\n", hostsFile)
        f = open("/etc/hosts", "w")
        f.write(hostsFile)
        f.close()
        
    def start(self):
        """Starts the GUI"""
        # Read the .stats file.   
        if not pathlib.Path(".stats").is_file():
            # If no .stats file is present, start the mainloop.
            # print(".stats file is not present")
            self.__generateParentWindow__()
        else:
            # .stats file is present.
            # print("*****.stats file is present*****")
            # Read the endtime
            endTime = 0
            try:
                endTime = int(open(".stats", "r").read())
                # print("End Time is ", endTime)
            except:
                endTime = 0
                # print("While fetching end time, error occurred, hence, setting end time to ", endTime)
            currentTime = time.time()
            if currentTime > endTime:
                # If cur_time > endtime, start the mainloop.
                # print("Current time is greater than endtime. Starting mainloop.")
                self.__generateParentWindow__()
            else:
                # Otherwise, display a box with remaining time.
                # print("Sites are still blocked.")
                self.initTimer(endTime - currentTime)
        self.parentWindow.mainloop()

    def initTimer(self, timeLeft):
        self.timeLeft = int(timeLeft)
        """Method initialises a timer"""
        # Create a timer window here
        self.__generateTimerWindow__()
        self.startTimer()
        
    def startTimer(self):
        """Method starts the timer"""
        if self.timeLeft == 0:
            # Delete contents from .stats
            open(".stats", "w").close()
            self.__clearParentWindowCanvas__()
            # Copy back /etc/.hosts.backup to /etc/hosts
            try:
                
                shutil.copy2("/etc/.hosts.backup", "/etc/hosts")
            except Exception as e:
                # print("While copying /etc/.hosts.backup to /etc/hosts, error is ", e)
                pass
            reloadDNS()
            self.start()
        else:
            self.timeLeft -= 1
            self.timerWindowLabel.config(text=str(self.timeLeft))
            self.timerWindowLabel.after(10, self.startTimer)
    
    def startButtonAction(self):
        """Called when the start button is pressed"""
        # Ask for sudo permission
        # try:
        #     subprocess.check_call(["gksudo", "su"])
        # except subprocess.CalledProcessError:
        #     messagebox.showinfo("message", "OOOOPS...\nWrong password!")
        #     return
        # else:
        #     messagebox.showinfo("message", "Login successful!")



        # Fetch the time in the slider
        timerVal = self.slider.get()
        # print("Timer value is ", timerVal)
        # Read all the sites in .domains.list. 
        if not pathlib.Path(".domains.list").is_file():
            # Create an .domains.list file here
            open(".domains.list", "w").close()
        # Read all domains
        domainsFile = open(".domains.list", "r").read()
        if domainsFile == "":
            # If no .domains.list file is present, display a messagebox stating so.
            messagebox.showerror("FocusApp Error", "No domains added yet. Add them by clicking the View button.")
            return
        
        # Make a backup of /etc/hosts to /etc/.hosts.backup
        try:
            open("/etc/.hosts.backup", "w").close()
            shutil.copy2("/etc/hosts", "/etc/.hosts.backup")
        except Exception as e:
            # print("While copying /etc/hosts to /etc/.hosts.backup, error is ", e)
            pass
        
        self.__writeToHosts__()

        reloadDNS()

        # Create a .stats file, with endtime
        curTime = int(time.time())
        endTime = curTime + int(timerVal * 3600)
        f = open(".stats", "w")
        f.write(str(endTime))
        f.close()
        # Call initTimer here
        self.initTimer(endTime - curTime)
        

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
        if not pathlib.Path(".domains.list").is_file():
            # Create an .domains.list file here
            open(".domains.list", "w").close()
        # Read all domains
        domainsList = open(".domains.list", "r").read().split("\n")
        # Prepend to the list
        domainsList.insert(0, domain)
        # Write to the file
        domainsFile = open(".domains.list", "w")
        domainsFile.write("\n".join(domainsList))
        domainsFile.close()
        self.__displayAllDomainsInListBox__()

    def deleteMenuAction(self):
        """Called when the delete context menu is clicked"""
        value = self.listBox.get(self.listBox.curselection()[0])
        if value == "":
            return
        # Read the file and store all the elements in a list
        domainsList = open(".domains.list", "r").read().split("\n")
        domainsList.remove(value)
        domainsFile = open(".domains.list", "w")
        domainsFile.write("\n".join(domainsList))
        domainsFile.close()
        self.__displayAllDomainsInListBox__()


def reloadDNS():
    """Function that reloads the /etc/hosts file"""
    return

"""
TODO
5. Use grid to restyle the app.
9. Check how to ask for permission for sudo usage.
11. Make the code portable to work on windows as well.
12. Set after() time to 1000, from 1.
"""