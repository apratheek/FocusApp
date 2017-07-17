import tkinter
from tkinter import messagebox
import functions

def startButtonAction():
    messagebox.showinfo("Say Hello", "Hello World")
    print("About to copy the sites list")

def viewButtonAction():
    # Display a listbox window
    functions.generateViewSitesFrame()
    # messagebox.showinfo("View List", "List will be displayed")

def addButtonAction():
    messagebox.showinfo("View List", "List will be displayed")