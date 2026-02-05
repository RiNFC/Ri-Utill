import tkinter as tk
import pytube.download_helper as dh
import os
import shutil

root = tk.Tk()
root.title("Youtube Downloader")
root.config(bg="black")
root.geometry("290x190")
root.resizable(False, False)

url_var = tk.StringVar()

def download():
    try: dh.download_video(url_var.get())
    except KeyError: pass
    files = os.listdir("./videos")
    videopath = files[0]
    shutil.move(f"./videos/{videopath}", "C:/Users/Ri/Videos/Youtube/Ri-util")

return_text = tk.Label(root, text="gay\n balls", bg="black", fg="yellow")
return_text.pack(anchor="n")

url_entry = tk.Entry(root, textvariable=url_var, width=100, bg="yellow")
url_entry.pack(side="bottom", pady=10)

download_button = tk.Button(root, text="Download", command=download, bg="yellow")
download_button.pack(side="bottom")


root.mainloop()