from tkinter import *
from tkinter import filedialog, ttk
from tkinter.messagebox import showerror, askyesno

filename = None
is_modified = False

def on_text_change(event=None):
    global is_modified

    if event.keysym in ("Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R", "s") and event.state & 0x4:
        return
    
    if not is_modified:
        is_modified = True
        update_status("Unsaved")

    if event.keysym in ("space", "Return", "BackSpace", "Delete"):
        text.edit_separator()

def update_status(status_text):
    status_label.config(text=f"Status: {status_text}")
    status_label.update_idletasks()

def newFile():
    global filename, is_modified
    if is_modified:
        confirm = askyesno("Unsaved Changes", "You have unsaved changes. Do you want to continue?")
        if not confirm:
            return
        
    filename = None
    is_modified = False
    update_status("Unsaved")
    text.delete(0.0, END)
    text.focus()

def saveFile(event=None):
    global filename, is_modified
    if filename:
        try:
            t = text.get(0.0, END)
            with open(filename, 'w', encoding="utf-8") as f:
                f.write(t.rstrip())
            is_modified = False
            update_status("Saved")
        except Exception as e:
            showerror(title="Error", message=f"Unable to save file: {e}")
    else:
        saveAs()

def saveAs():
    global filename, is_modified
    filename = filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    if not filename:
        return

    t = text.get(0.0, END)
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(t.rstrip())
        is_modified = False
        update_status("Saved")
    except Exception as e:
        showerror(title="Error", message=f"Unable to save file: {e}")

def openFile():
    global filename
    f = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    if not f:
        return
    
    filename = f
    
    with open(f, "r", encoding="utf-8") as file:
        t = file.read()

    text.delete(0.0, END)
    text.insert(0.0, t)
    text.focus()

def undoText(event=None):
    global is_modified
    try:
        text.edit_undo()
        is_modified = True
        update_status("Unsaved")
    except Exception as e:
        pass

def redoText(event=None):
    global is_modified
    try:
        text.edit_redo()
        is_modified = True
        update_status("Unsaved")
    except Exception as e:
        pass
    
root = Tk()
root.title("Ouroboros Text Editor")
root.geometry("400x400")
root.resizable(True, True)

#Frame for text and scrollbar
text_frame = Frame(root)
text_frame.pack(expand=True, fill=BOTH)

#scrollbar
scrollbar = Scrollbar(text_frame)
scrollbar.pack(side=RIGHT, fill=Y)

#Sizegrip
my_sizegrip = ttk.Sizegrip(root)
my_sizegrip.pack(side="right", anchor=SE)

# Toolbar
toolbar = Frame(text_frame)
toolbar.pack(side=TOP, fill=X, padx=5, pady=5)

# Toolbar buttons
undo_btn = Button(toolbar, text="Undo", command=undoText)
undo_btn.pack(side=LEFT, padx=2, pady=2)

redo_btn = Button(toolbar, text="Redo", command=redoText)
redo_btn.pack(side=LEFT, padx=2, pady=2)

# Text
text = Text(text_frame, height=20, width=50, undo=True, yscrollcommand=scrollbar.set)
text.pack(expand=True, fill=BOTH)
scrollbar.config(command=text.yview)

# Key Mapping
text.bind("<KeyRelease>", on_text_change)
text.bind_all("<Control-z>", undoText)
text.bind_all("<Control-y>", redoText)
text.bind_all("<Control-s>", lambda event: saveFile())

status_label = Label(root, text="Status: Saved", anchor=W, relief=SUNKEN)
status_label.pack(side=BOTTOM, fill=X)

# Menu Bar
menubar = Menu(root)
filemenu = Menu(menubar)
filemenu.add_command(label="New", command=newFile)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_command(label="Save", command=saveFile)
filemenu.add_command(label="Save As", command=saveAs)
filemenu.add_separator()
filemenu.add_command(label="Quit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

root.config(menu=menubar)
root.mainloop()