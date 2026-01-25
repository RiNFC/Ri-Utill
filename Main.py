from pypresence import Presence
import time
import psutil
import sys
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import threading
import requests
import dotenv
import os



dotenv.load_dotenv()
disc_token = os.getenv("disctoken")


start = time.time()
rpc_stop_event = threading.Event()

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
    start_discfm()
    start_rpc()
    icon.run()
    


def rpc():
    global rpc_stop_event
    rpc_stop_event.clear()
    def get_speeds(interval=1):
        net1 = psutil.net_io_counters()
        time.sleep(interval)
        net2 = psutil.net_io_counters()

        down = (net2.bytes_recv - net1.bytes_recv) * 8 / interval / 1_000_000
        up = (net2.bytes_sent - net1.bytes_sent) * 8 / interval / 1_000_000

        return down, up

    CLIENT_ID = "1428085437213179954"

    rpc = Presence(CLIENT_ID, pipe=0)
    rpc.connect()
    
    while not rpc_stop_event.is_set():
        download_speed, upload_speed = get_speeds()
        try: rpc.update(
        state=f"Dwn /|{download_speed:.2f} Mbps|\ ".removesuffix(" "),
        details=f"Up /|{upload_speed:.2f} Mbps|\ ".removesuffix(" "),
        large_image="cpu",
        small_image="chair",
        small_text="Chair.",
        large_text="Sanctitas tua",
        start=start,
        buttons=[{"label": "VRChat", "url": "https://vrchat.com/home/user/usr_bd418c2c-216e-40cf-b072-26574d66f065"}]
        )
        except: break
        time.sleep(1)
    rpcthread = threading.Thread(target=rpc, daemon=True)

def discfm():
    global icon
    baseuserdata = []
    index = 0
    scanfirst = True
    scanindex = 0
    while True:
        if index == 0:
            response = requests.get("https://discord.com/api/v9/users/@me/relationships", headers={"authorization": disc_token})
            friends_json = response.json()
            for f in friends_json: print(f["user"]["username"])
            index += 1
            print("base rela scan complete")

        scanindex = 0
        for friend_json in friends_json:
            response2 = requests.get(f"https://discord.com/api/v9/users/{friend_json["user"]["id"]}/profile", headers={"authorization": disc_token})
            if response2.status_code != 200: 
                time.sleep(6)
                response2 = requests.get(f"https://discord.com/api/v9/users/{friend_json["user"]["id"]}/profile", headers={"authorization": disc_token})
                if response2.status_code != 200:
                    print("skipping Invalid")
                    continue

            friend = response2.json()["user"]
            if scanfirst:
                baseuserdata.append(friend)
                print("added data to base data")
            if not scanfirst:
                print("checking user data")
                if friend != baseuserdata[scanindex]:
                    icon.notify(f"{friend["global_name"]} has Changed their Profile")
                    baseuserdata.pop(scanindex)
                    baseuserdata.insert(scanindex, friend)
            scanindex += 1
            time.sleep(2)
        
        scanfirst = False
        
        time.sleep(30)

        if index > 3:
            index = 0


rpcthread = threading.Thread(target=rpc, daemon=True)
discfmthread = threading.Thread(target=discfm, daemon=True)
def start_rpc():
    global rpc_stop_event
    global rpcthread

    rpc_stop_event.set()
    try: rpcthread.join()
    except RuntimeError: pass

    rpcthread.start()

def start_discfm():
    discfmthread.start()

menu = Menu(MenuItem("Exit", on_exit), MenuItem("Restart RPC", start_rpc))
icon = Icon(
    "Ri Utils",
    create_image(),
    "Ri Utils",
    menu
)


setup_tray()
