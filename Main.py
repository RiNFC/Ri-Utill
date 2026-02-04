import time
import sys
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import threading
import dotenv
import os
import Addons.rpc as rpc
import Addons.discfm as discfm
from flask import Flask, request
import signal
import requests

app = Flask(__name__)





# TODO
#
# 1, Finish Notify Function for Addons (Addon for the Addons)
#
# 2, Put yt downloader gui into Utils
#


dotenv.load_dotenv()
disc_token = os.getenv("disctoken")
start = int(time.time())

def create_image():
    image = Image.new("RGB", (64, 64), "black")
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, 48, 48), fill="yellow")
    return image

########### FUCKING FIX LATER ############
#def restart_rpc():
    #global rpcthread
    #rpcthread = threading.Thread(target=rpc, daemon=True)
    #start_rpc()
########### FUCKING FIX LATER ############



arfa = []
def on_exit(icon, item):
    global arfa
    for targ in arfa:
        targ[0].set()
    requests.post("http://127.0.0.1:5000/shutdown")
    icon.stop()
    sys.exit()

menu = Menu(MenuItem("Exit", on_exit))
icon = Icon(
    "Ri Utils",
    create_image(),
    "Ri Utils",
    menu
)

icon.notify
@app.route('/shutdown', methods=['POST'])
def shutdown():
    os.kill(os.getpid(), signal.SIGINT)

@app.route('/notify', methods=['POST'])
def notification():
    global icon
    content = request.form.get('content')
    if content:
        icon.notify(content)
        return 'Command received', 200
    return 'No command received', 400

addon_run_functions = [rpc.run, discfm.run]
addon_run_functions_args = [(start,), (disc_token, icon)]
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
    app.run(host='127.0.0.1', port=5000)


setup_tray()