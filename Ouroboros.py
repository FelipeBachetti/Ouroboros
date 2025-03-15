from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showerror

filename = None

def newFile():
    global filename
    filename = None
    text.delete(0.0, END)

def saveFile():
    global filename
    if filename:
        try:
            t = text.get(0.0, END)
            with open(filename, 'w', encoding="utf-8") as f:
                f.write(t.rstrip())
        except Exception as e:
            showerror(title="Error", message=f"Unable to save file: {e}")
    else:
        saveAs()

def saveAs():
    global filename
    filename = filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    if not filename:
        return

    t = text.get(0.0, END)
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(t.rstrip())
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
    
root = Tk()
root.title("Ouroboros Text Editor")
root.minsize(width=400, height=400)
root.maxsize(width=400, height=400)

text = Text(root, height=400, width=400)
text.pack()

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