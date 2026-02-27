import time
import sys
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import threading
import dotenv
import os
import Addons.rpc as rpc
from Addons.notify import notify
from flask import Flask, request
import signal
import requests
import subprocess
import json


app = Flask(__name__)

dotenv.load_dotenv()
disc_token = os.getenv("disctoken")
webhook = os.getenv("webhook")

dr = False
curt = time.time()
if os.path.exists(".timecache"):
    with open(".timecache", "r") as file:
        data = json.load(file)
        timed = data["end"]
        if timed + 300 > curt:
            start = data["ts"]
            dr = True
        else: start = curt
else: start = curt
if dr: os.remove(".timecache")



if os.path.exists(".load"):
    with open(".load", "r") as file:
        data = json.load(file)
    start = data["time"]
    os.remove(".load")

def start_ytd():
    subprocess.Popen(
        [sys.executable, "Addons/ytdownloader.py"],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

def dt():
    subprocess.Popen(
        [sys.executable, "Addons/msgloaderopener.py"],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

arfa = []
def on_exit(icon, item):
    global arfa
    for targ in arfa:
        targ[0].set()
    with open(".timecache", "w") as file:
        json.dump({"ts": start, "end": time.time()}, file)
    requests.post("http://127.0.0.1:5766/shutdown")
    

menu = Menu(MenuItem("YT Downloader", start_ytd), MenuItem("Discord_Tools", dt), MenuItem("Exit", on_exit))
icon = Icon(
    "Ri Utils",
    Image.open("icon/Icon.png"),
    "Ri Utils",
    menu
)


@app.route('/shutdown', methods=['POST'])
def shutdown():
    os.kill(os.getpid(), signal.SIGINT)
    
@app.route('/notify', methods=['POST'])
def notification():
    global icon
    data = request.json
    if not data:
        return 'No command received', 400
    
    content = data.get('content')
    title = data.get('title')

    if content:
        icon.notify(content, title)
        return 'Command received', 200
    
    return 'No command received', 400



addon_run_functions = [rpc.run]
addon_names = ["RPC"]
addon_run_functions_args = [(start,)]
addon_threads = []



def gen_threads():
    index = 0
    for arf in addon_run_functions:
        args = addon_run_functions_args.pop(index)
        list_args = list(args)
        list_args.insert(0, threading.Event())
        addon_run_functions_args.insert(index, tuple(list_args))
        addon_threads.append(threading.Thread(target=arf, args=addon_run_functions_args[index], daemon=True))
        index += 1

def setup_tray():
    global icon
    global addon_threads
    global arfa
    arfa = addon_run_functions_args
    gen_threads()
    for thread in addon_threads:
        thread: threading.Thread
        thread.start()
        
    icon_thread = threading.Thread(target=icon.run, daemon=True)
    icon_thread.start() 
    app.run(host='0.0.0.0', port=5766)



setup_tray()