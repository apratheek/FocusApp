import actions
import functions
import tkinter

# -----------------------------------------------------
# Check here if the block is still active
# If active, then display a window with a timer
# Otherwise, display a selection window

# -----------------------------------------------------
# Parent Window
# Create the parent window
parentWindow = functions.generateParentWindow(tkinter.Tk())

# Bind the slider
functions.generateSlider(parentWindow)
# Bind the Start button
functions.generateStartButton(parentWindow)
# Bind the View button
functions.generateViewButton(parentWindow)

# -----------------------------------------------------
# Listbox window
# Create a window
# Attach a listbox that displays all the sites
# Attach an Entry widget that can accept text
# Attach a ADD button 


# -----------------------------------------------------
# Actions
# Attach an event handler to the view button to display a listbox with all the sites
# Attach an event handler to the start button that will take all the sites mentioned and rewrite the /etc/hosts file
# Attach an event handler to the add button that will take the text in the entry widget and add it to the listbox
# Attach a context menu to the listbox that will have a function to remove the item from the listbox

# Start
parentWindow.mainloop()