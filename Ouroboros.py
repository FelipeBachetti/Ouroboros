from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showerror, askyesno

filename = None
is_modified = False

def on_text_change(event=None):
    global is_modified
    is_modified = True

def newFile():
    global filename, is_modified
    if is_modified:
        confirm = askyesno("Unsaved Changes", "You have unsaved changes. Do you want to continue?")
        if not confirm:
            return
        
    filename = None
    text.delete(0.0, END)
    text.focus()

def saveFile():
    global filename, is_modified
    if filename:
        try:
            t = text.get(0.0, END)
            with open(filename, 'w', encoding="utf-8") as f:
                f.write(t.rstrip())
            is_modified = False
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
    
root = Tk()
root.title("Ouroboros Text Editor")
root.minsize(width=400, height=400)
root.maxsize(width=400, height=400)

text = Text(root, height=400, width=400)
text.pack()
text.bind("<KeyRelease>", on_text_change)

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