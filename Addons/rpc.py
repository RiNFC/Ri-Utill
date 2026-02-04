import psutil
import time
from pypresence import Presence

start = time.time()

def run(*args):
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
    
    while not args[0].is_set():
        download_speed, upload_speed = get_speeds()
        try: rpc.update(
        state=f"Dwn /|{download_speed:.2f} Mbps|\ ".removesuffix(" "),
        details=f"Up /|{upload_speed:.2f} Mbps|\ ".removesuffix(" "),
        large_image="cpu",
        small_image="chair",
        small_text="Chair.",
        large_text="Sanctitas tua",
        start=args[1],
        buttons=[{"label": "VRChat", "url": "https://vrchat.com/home/user/usr_bd418c2c-216e-40cf-b072-26574d66f065"}, {"label": "null", "url": "https://ri-rye.xyz"}]
        )
        except: break
        time.sleep(1)