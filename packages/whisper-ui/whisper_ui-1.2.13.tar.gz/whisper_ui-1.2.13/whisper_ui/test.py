import os, re
from tkinter import TOP, Entry, Label, StringVar
from tkinterdnd2 import *


def drop_file(event):
    raw_data = event.data.strip()

    # Extract file paths: Matches either {wrapped path} or plain paths
    files = re.findall(r'(\{.*?\})', raw_data)
    
    # remove each match from the raw data
    for file in files:
        raw_data = raw_data.replace(file, '')
        
    # split on whitespace - default .split() handles multiple spaces/trailing spaces
    files += raw_data.split()
    
    final_files = []
    for i in range(len(files)):
        files[i] = files[i].replace('{', '').replace('}', '').strip()
        if files[i]:
            final_files.append(files[i])
    
    for file in files:
        assert os.path.exists(file), f'File {file} does not exist.'

    # Convert to a semicolon-separated string
    formatted_paths = ";".join(files)

    # Update the entry field
    entryWidget.delete(0, len(entryWidget.get()))
    entryWidget.insert(0, formatted_paths)

root = TkinterDnD.Tk()
root.geometry("350x100")
root.title("Get file path")

nameVar = StringVar()

entryWidget = Entry(root)
entryWidget.pack(side=TOP, padx=5, pady=5, fill='x', expand=True)

pathLabel = Label(root, text="Drag and drop file in the entry box")
pathLabel.pack(side=TOP)

entryWidget.drop_target_register(DND_ALL)
entryWidget.dnd_bind("<<Drop>>", lambda event: drop_file(event))

root.mainloop()