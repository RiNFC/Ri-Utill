from pypresence import Presence
import time
import psutil
import sys
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import threading


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
    menu = Menu(MenuItem("Exit", on_exit))
    icon = Icon(
        "Ri Utils",
        create_image(),
        "Ri Utils",
        menu
    )
    icon.run()


start = time.time()
def rpc():
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
    
    while True:
        download_speed, upload_speed = get_speeds()
        rpc.update(
        state=f"Dwn /|{download_speed:.2f} Mbps|\ ".removesuffix(" "),
        details=f"Up /|{upload_speed:.2f} Mbps|\ ".removesuffix(" "),
        large_image="cpu",
        small_image="chair",
        small_text="Chair.",
        large_text="Sanctitas tua",
        start=start,
        buttons=[{"label": "VRChat", "url": "https://vrchat.com/home/user/usr_bd418c2c-216e-40cf-b072-26574d66f065"}]
        )
        time.sleep(3)


rpcthread = threading.Thread(target=rpc, daemon=True)
rpcthread.start()
setup_tray()
