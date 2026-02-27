import psutil
import time
from pypresence import Presence


def vrchat_running_via_steam():
    for proc in psutil.process_iter(['name', 'ppid']):
        try:
            if proc.info['name'] == "VRChat.exe":
                parent = psutil.Process(proc.info['ppid'])
                if parent.name().lower() == "steam.exe":
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied): pass
    return False

def get_speeds(interval=1):
    net1 = psutil.net_io_counters()
    time.sleep(interval)
    net2 = psutil.net_io_counters()

    down = (net2.bytes_recv - net1.bytes_recv) * 8 / interval / 1_000_000
    up = (net2.bytes_sent - net1.bytes_sent) * 8 / interval / 1_000_000

    return down, up


def run(*args):
    CLIENT_ID = "1428085437213179954"

    rpc = Presence(CLIENT_ID, pipe=0)
    rpc.connect()

    vrchat_active = False 

    while not args[0].is_set():
        if vrchat_running_via_steam():

            if not vrchat_active:
                print("VRChat detected — clearing activity")
                try: rpc.clear()
                except: pass
                vrchat_active = True

            time.sleep(3)
            continue

        else:
            if vrchat_active:
                print("VRChat closed — restoring activity")
                vrchat_active = False
        download_speed, upload_speed = get_speeds()

        try:
            rpc.update(
                state=f"Dwn /|{download_speed:.2f} Mbps|\\",
                details=f"Up /|{upload_speed:.2f} Mbps|\\",
                large_image="cpu",
                small_image="chair",
                small_text="Chair.",
                large_text="Sanctitas tua",
                start=args[1],
                buttons=[
                    {
                        "label": "VRChat",
                        "url": "https://vrchat.com/home/user/usr_bd418c2c-216e-40cf-b072-26574d66f065"},
                    {
                        "label": "null",
                        "url": "https://ri-rye.xyz"}])
        except: break

        time.sleep(1)