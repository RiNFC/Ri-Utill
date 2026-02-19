import tkinter as tk
import os
import signal
from tkinter.filedialog import askopenfilename
import shutil
import subprocess
import sys


def file_select():
    file_types = (
    ("Json files", "*.json"),
    ("All files", "*.*")
    )
    
    path = askopenfilename(filetypes=file_types)
    name = path.split("/")[len(path.split("/"))-1]
    try: os.remove("./discord_messages.json")
    except: pass
    shutil.copy(path, "./")
    os.rename(f"./{name}", "discord_messages.json")

def open_viewer():
    subprocess.Popen(
        [sys.executable, "./msgloader/viewer.py"],
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    os.kill(os.getpid(), signal.SIGINT)

def open_logger():
    subprocess.Popen(
        [sys.executable, "./addons/logopen.py"],
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    os.kill(os.getpid(), signal.SIGINT)

root = tk.Tk()
root.title("Opener")
root.config(bg="black")
root.iconbitmap("icon/icon.ico")
root.geometry("290x190")
root.resizable(False, False)

file_button = tk.Button(root, text="File", command=file_select, bg="yellow")
file_button.pack(side="top")

viewer_button = tk.Button(root, text="Viewer", command=open_viewer, bg="yellow")
viewer_button.pack(side="bottom")

logger_button = tk.Button(root, text="Logger", command=open_logger, bg="yellow")
logger_button.pack(side="bottom")

root.mainloop()