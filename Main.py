from pypresence import Presence
import time
import sys
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import threading
import dotenv
import os
import Addons.rpc as rpc
import Addons.discfm as discfm


dotenv.load_dotenv()
disc_token = os.getenv("disctoken")
start = int(time.time())

addon_run_functions = [rpc.run, discfm.run]
addon_run_functions_args = [(start,), (disc_token,)]
addon_run_functions_exit_events = [threading.Event(), threading.Event()]
addon_threads = []


def gen_threads():
    index = 0
    for arf in addon_run_functions:
        args = addon_run_functions_args.pop(index)
        list_args = list(args)
        list_args.insert(0, addon_run_functions_exit_events[index])
        addon_run_functions_args.insert(index, tuple(list_args))
        addon_threads.append(threading.Thread(target=arf, args=addon_run_functions_args[index]))
        index += 1



def on_exit(icon, item):
    global running
    running = False
    icon.stop()
    sys.exit()
def create_image():
    image = Image.new("RGB", (64, 64), "black")
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, 48, 48), fill="yellow")
    return image

def setup_tray():
    global icon
    global addon_threads
    gen_threads()
    for thread in addon_threads:
        thread: threading.Thread
        thread.start()
        
    icon.run()


########### FUCKING FIX LATER ############
#def restart_rpc():
    #global rpcthread
    #rpcthread = threading.Thread(target=rpc, daemon=True)
    #start_rpc()
########### FUCKING FIX LATER ############


menu = Menu(MenuItem("Exit", on_exit))
icon = Icon(
    "Ri Utils",
    create_image(),
    "Ri Utils",
    menu
)


setup_tray()
