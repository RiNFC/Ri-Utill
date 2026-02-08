import tkinter as tk
import pytube.download_helper as dh
import os
import shutil
import re, requests
from urllib.parse import urlparse

def check_youtube_url(url, timeout=5):
    try:
        if not all(urlparse(url)[:2]):
            return 3
    except:
        return 3

    m = re.search(r"(youtube\.com|youtu\.be)/(watch\?v=|embed/|shorts/)?([A-Za-z0-9_-]{11})", url)
    if not m:
        return 2

    try:
        r = requests.get(
            "https://www.youtube.com/oembed",
            params={"url": f"https://www.youtube.com/watch?v={m.group(3)}"},
            timeout=timeout,
        )
        return 0 if r.status_code == 200 else 1
    except:
        return 1


root = tk.Tk()
root.title("Youtube Downloader")
root.config(bg="black")
root.iconbitmap("icon/icon.ico")
root.geometry("290x190")
root.resizable(False, False)

url_var = tk.StringVar()

def download():
    res = check_youtube_url(url_var.get())
    match res:
        case 0:
            try: dh.download_video(url_var.get())
            except KeyError: pass
            files = os.listdir("./videos")
            videopath = files[0]
            shutil.move(f"./videos/{videopath}", "C:/Users/Ri/Videos/Youtube/Ri-util")
            return_text.config(text=f"Successfully downloaded:\n{videopath}\nCopied to Clipboard")
            os.system(f'powershell Set-Clipboard -Path C:/Users/Ri/Videos/Youtube/Ri-util/{videopath}')
        case 1: return_text.config(text="Invalid Youtube Video")
        case 2: return_text.config(text="Not a Youtube Video URL")
        case 3: return_text.config(text="Not a Valid URL")

return_text = tk.Label(root, text="YT Video Downloader", bg="black", fg="yellow")
return_text.pack(anchor="n")

url_entry = tk.Entry(root, textvariable=url_var, width=100, bg="yellow")
url_entry.pack(side="bottom", pady=10)

download_button = tk.Button(root, text="Download", command=download, bg="yellow")
download_button.pack(side="bottom")


root.mainloop()